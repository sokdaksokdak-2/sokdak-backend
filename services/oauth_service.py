from fastapi import Request
from fastapi.responses import JSONResponse
import httpx
from sqlalchemy.orm import Session
from models.member import Member
from models.member_oauth import  OAuthProvider
from core.config import settings
import logging
from crud import member_oauth as member_oauth_crud
from crud import member as member_crud
from core.token import TokenService as token_service
from schemas.auth import LoginResponseDto
logger = logging.getLogger(__name__)

class OAuthConfig:
    """OAuth 설정 관리 클래스"""

    class Google:
        CLIENT_ID = settings.google_client_id
        REDIRECT_URI = settings.google_redirect_uri
        CLIENT_SECRET = settings.google_client_secret
        TOKEN_URL = "https://oauth2.googleapis.com/token"
        USERINFO_URL = "https://www.googleapis.com/oauth2/v1/userinfo"

    class Kakao:
        CLIENT_ID = settings.kakao_client_id
        REDIRECT_URI = settings.kakao_redirect_uri
        TOKEN_URL = "https://kauth.kakao.com/oauth/token"
        USERINFO_URL = "https://kapi.kakao.com/v2/user/me"

    class Naver:
        CLIENT_ID = settings.naver_client_id
        REDIRECT_URI = settings.naver_redirect_uri
        CLIENT_SECRET = settings.naver_client_secret
        TOKEN_URL = "https://nid.naver.com/oauth2.0/token"
        USERINFO_URL = "https://openapi.naver.com/v1/nid/me"

    
class OAuthErrorMessages:
    """OAuth 에러 메시지 상수"""
    MISSING_CODE = "Authorization code is missing"
    INVALID_PROVIDER = "Unsupported OAuth provider: {}"
    MISSING_USER_INFO = "Required user information not found in {} response"
    TOKEN_FAILED = "Failed to get access token from {}"

class OAuthError(Exception):
    """OAuth 인증 과정에서 발생하는 예외를 처리하는 클래스
    
    Args:
        message: 에러 메시지
        provider: OAuth 프로바이더 (google, kakao, naver)
        status_code: HTTP 상태 코드 (기본값: 400)
    """
    def __init__(self, message: str, provider: str = None, status_code: int = 400):
        self.message = message.format(provider) if provider else message
        self.status_code = status_code
        self.provider = provider


class OAuthResponse:
    """OAuth 응답을 표준화하는 클래스"""
    
    @staticmethod
    def success(member: Member, access_token: str, refresh_token: str = None):
        """성공 응답을 생성

        Args:
            user: 사용자 정보
            access_token: 액세스 토큰
            refresh_token: 리프레시 토큰 (선택사항)

        Returns:
            JSONResponse: 표준화된 성공 응답
        """
        return LoginResponseDto(
            access_token=access_token,
            refresh_token=refresh_token,
            member_seq=member.member_seq,
            nickname=member.nickname or "",
            email=member.email
        )

    @staticmethod
    def error(message: str, status_code: int = 400):
        return JSONResponse(
            {"status": "error", "message": message},
            status_code=status_code
        )

# TODO :utils/oauth_paser.py로 분리 예정
class OAuthUserInfoParser:
    """OAuth 제공자별 사용자 정보 파싱 클래스"""
    @staticmethod
    def parse_google(userinfo: dict) -> dict:
        return {
            "email": userinfo.get("email"),
            "oauth_id": userinfo.get("id") or userinfo.get("sub"),
            "nickname": userinfo.get("email")
        }

    @staticmethod
    def parse_kakao(userinfo: dict) -> dict:
        return {
            "email": userinfo.get("kakao_account", {}).get("email"),
            "oauth_id": str(userinfo.get("id")),
            "nickname": userinfo.get("kakao_account", {}).get("profile", {}).get("nickname")
        }

    @staticmethod
    def parse_naver(userinfo: dict) -> dict:
        response = userinfo.get("response", {})
        return {
            "email": response.get("email"),
            "oauth_id": response.get("id"),
            "nickname": response.get("nickname")
        }

class OAuthService:
    """OAuth 인증을 처리하는 서비스 클래스"""
    def __init__(self, db: Session):
        self.db = db
        self.token_service = token_service()

    
    def get_oauth_provider_info(self, provider: str):
        if provider == "google":
            return {
                "token_url": OAuthConfig.Google.TOKEN_URL,
                "userinfo_url": OAuthConfig.Google.USERINFO_URL,
                "token_params": {
                    "client_id": OAuthConfig.Google.CLIENT_ID,
                    "client_secret": OAuthConfig.Google.CLIENT_SECRET,
                    "redirect_uri": OAuthConfig.Google.REDIRECT_URI,
                }
            }
        elif provider == "kakao":
            return {
                "token_url": OAuthConfig.Kakao.TOKEN_URL,
                "userinfo_url": OAuthConfig.Kakao.USERINFO_URL,
                "token_params": {
                    "client_id": OAuthConfig.Kakao.CLIENT_ID,
                    "redirect_uri": OAuthConfig.Kakao.REDIRECT_URI,
                }
            }
        elif provider == "naver":
            return {
                "token_url": OAuthConfig.Naver.TOKEN_URL,
                "userinfo_url": OAuthConfig.Naver.USERINFO_URL,
                "token_params": {
                    "client_id": OAuthConfig.Naver.CLIENT_ID,
                    "client_secret": OAuthConfig.Naver.CLIENT_SECRET,
                    "redirect_uri": OAuthConfig.Naver.REDIRECT_URI,
                }
            }
        raise OAuthError(f"Unsupported OAuth provider: {provider}")

    # TODO : 이 get_access_token은 뭘까
    async def get_access_token(self, code: str, token_url: str, token_params: dict) -> str:
        async with httpx.AsyncClient() as client:
            token_response = await client.post(
                token_url,
                data={
                    **token_params,
                    "code": code,
                    "grant_type": "authorization_code"
                },
                headers={"Content-Type": "application/x-www-form-urlencoded;charset=utf-8"}
            )
        token_data = token_response.json()
        access_token = token_data.get("access_token")
        
        if not access_token:
            raise OAuthError("Failed to get access token")
        
        return access_token

    
    async def get_user_info(self,access_token: str, userinfo_url: str) -> dict:
        async with httpx.AsyncClient() as client:
            userinfo_response = await client.get(
                userinfo_url,
                headers={"Authorization": f"Bearer {access_token}"}
            )
        return userinfo_response.json()

    # 소셜 로그인 처리
    async def process_oauth_user(self, db, userinfo: dict, provider: str):
        if provider == "google":
            email = userinfo.get("email")
            oauth_id = userinfo.get("id") or userinfo.get("sub")
            nickname = email  # Google API에서 nickname 정보가 없는 경우
        elif provider == "kakao":
            email = userinfo.get("kakao_account", {}).get("email")
            oauth_id = str(userinfo.get("id"))
            nickname = userinfo.get("kakao_account", {}).get("profile", {}).get("nickname", email)
        elif provider == "naver":
            email = userinfo.get("response", {}).get("email")
            oauth_id = userinfo.get("response", {}).get("id")
            nickname = userinfo.get("response", {}).get("nickname")
        else:
            raise OAuthError(f"Unsupported OAuth provider: {provider}")

        if not email or not oauth_id:
            raise OAuthError(f"Email or oauth_id not found in {provider} response")

        # OAuth 계정 확인
        oauth_account = member_oauth_crud.get_member_by_oauth(
            self.db, 
            OAuthProvider[provider.upper()], 
            oauth_id
        )

        if oauth_account:
            member = member_crud.get_member_by_member_seq(self.db, oauth_account.member_seq)
        else:
            # 이메일로 기존 회원 확인
            member = member_crud.get_member_by_email(self.db, email)
            if not member:
                # 신규 회원 가입
                member = member_crud.register_member(self.db, email, password=None)
            
            # OAuth 계정 연동
            member_oauth_crud.register_oauth_account(
                self.db, 
                OAuthProvider[provider.upper()], 
                oauth_id, 
                member.member_seq
            )

        # 토큰 발급
        access_token = self.token_service.create_access_token(member)
        refresh_token = self.token_service.create_refresh_token(member)
        
        return OAuthResponse.success(member, access_token, refresh_token)

    # 소셜 로그인 콜백 처리
    async def handle_oauth_callback(self, request: Request, provider: str):
        """OAuth 프로바이더의 콜백을 처리

        Args:
            request: FastAPI 요청 객체
            db: 데이터베이스 세션
            provider: OAuth 프로바이더 (google, kakao, naver)

        Returns:
            JSONResponse: 인증 결과 응답

        Raises:
            OAuthError: OAuth 인증 과정에서 발생하는 예외
        """
        try:
            logger.info(f"Processing OAuth callback for provider: {provider}")
            code = request.query_params.get("code")
            if not code:
                raise OAuthError("Missing code parameter")
            # TODO 
            provider_info = self.get_oauth_provider_info(provider)
            
            # 액세스 토큰 발급
            access_token = await self.get_access_token(
                code, 
                provider_info["token_url"], 
                provider_info["token_params"]
            )
            
            # 유저 정보 조회
            userinfo = await self.get_user_info(
                access_token, 
                provider_info["userinfo_url"]
            )
            
            # 회원 처리 및 JWT 토큰 발급
            return await self.process_oauth_user(self.db, userinfo, provider)
            
        except OAuthError as e:
            logger.error(f"OAuth error for {provider}: {e.message}")
            return OAuthResponse.error(e.message, e.status_code)
        except Exception as e:
            logger.exception(f"Unexpected error in OAuth callback for {provider}")
            return OAuthResponse.error(str(e), 500)    
    




        

