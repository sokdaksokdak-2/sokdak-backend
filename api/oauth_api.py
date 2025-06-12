# 소셜 로그인 API
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from services import OAuthService
from sqlalchemy.orm import Session
from db.session import get_session
from schemas.auth import LoginResponseDto
from utils.oauth_url_builder import OAuthLoginURLBuilder
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

SUPPORTED_PROVIDERS = ["google", "kakao","naver"]

# DI 주입 방식으로 변경
# TODO : 이후 dependencies/auth_dependencies.py 파일로 분리
def get_oauth_service(db: Session = Depends(get_session)) -> OAuthService:
    return OAuthService(db)


# OAuth 로그인 - 통합
@router.get("/login/{provider}",
            summary="OAuth 로그인 페이지로 리다이렉트 (google, kakao, naver)",
            description="{google, kakao, naver} OAuth 로그인 페이지로 리다이렉트",
        )
def oauth_login(provider: str):
    print("✅oauth api 접속")
    if provider not in SUPPORTED_PROVIDERS:
        raise HTTPException(status_code=400, detail="지원하지 않는 소셜 로그인입니다.")

    url_builder = OAuthLoginURLBuilder()

    if provider == "google":
        return RedirectResponse(url_builder.build_google_url())
    elif provider == "kakao":
        return RedirectResponse(url_builder.build_kakao_url())
    elif provider == "naver":
        return RedirectResponse(url_builder.build_naver_url())



# @router.get("/login/{provider}/callback",
#             summary="OAuth 콜백 처리(google, kakao, naver)",
#             response_model=LoginResponseDto,
#             dependencies=[Depends(get_oauth_service)],
#             response_description="{google, kakao, naver} OAuth 콜백 처리",
#             response_model_include={"access_token", "refresh_token","member_seq", "nickname"}
#         )
# async def oauth_callback(provider: str, request: Request, oauth_service: OAuthService = Depends(get_oauth_service)) :
    
#     return await oauth_service.handle_oauth_callback(request, provider)

@router.get("/login/{provider}/callback",
            summary="OAuth 콜백 처리(google, kakao, naver)",
            dependencies=[Depends(get_oauth_service)],
            )
async def oauth_callback(provider: str, request: Request, oauth_service: OAuthService = Depends(get_oauth_service)):
    # 기존 응답 받아오기 (JSON 형태)
    print("✅callback진입")
    login_data = await oauth_service.handle_oauth_callback(request, provider)

    if isinstance(login_data, JSONResponse):
        return login_data
 
    # 딥링크 URL 구성
    redirect_url = (
        f"myapp://api/oauth/callback"
        f"?access_token={login_data.access_token}"
        f"&refresh_token={login_data.refresh_token}"
        f"&member_seq={login_data.member_seq}"
        f"&nickname={login_data.nickname}"
        f"&email={login_data.email}"
    )
    logger.info(f"✅✅딥링크 : {redirect_url}")
 
    return RedirectResponse(url=redirect_url)
    # return login_data

