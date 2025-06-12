import urllib.parse
from services.oauth_service import OAuthConfig
import logging

logger = logging.getLogger(__name__)

class OAuthLoginURLBuilder:
    """OAuth 로그인 URL 생성을 담당하는 클래스"""
    
    @staticmethod
    def build_google_url() -> str:
        """Google OAuth 로그인 URL 생성"""
        logger.warning(f"🚨🚨🚨{OAuthConfig.Google.REDIRECT_URI}")
        params = {
            "client_id": OAuthConfig.Google.CLIENT_ID,
            "redirect_uri": OAuthConfig.Google.REDIRECT_URI,
            "response_type": "code",
            "scope": "openid email profile",
            "access_type": "offline",
            "prompt": "consent"  # refresh_token 발급을 위해 필요
        }
        return f"https://accounts.google.com/o/oauth2/v2/auth?{urllib.parse.urlencode(params)}"

    @staticmethod
    def build_kakao_url() -> str:
        """Kakao OAuth 로그인 URL 생성"""
        params = {
            "client_id": OAuthConfig.Kakao.CLIENT_ID,
            "redirect_uri": OAuthConfig.Kakao.REDIRECT_URI,
            "response_type": "code",
            "scope": "account_email profile_nickname"
        }
        return f"https://kauth.kakao.com/oauth/authorize?{urllib.parse.urlencode(params)}"

    @staticmethod
    def build_naver_url() -> str:
        """Naver OAuth 로그인 URL 생성"""
        params = {
            "client_id": OAuthConfig.Naver.CLIENT_ID,
            "redirect_uri": OAuthConfig.Naver.REDIRECT_URI,
            "response_type": "code",
            "scope": "email nickname"
        }
        return f"https://nid.naver.com/oauth2.0/authorize?{urllib.parse.urlencode(params)}"
