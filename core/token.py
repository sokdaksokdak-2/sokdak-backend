# core/token.py 
# JWT 토큰 발급/ 검증 관련 로직
from core.config import settings
from datetime import datetime, timedelta, UTC
from models.member import Member
import jwt

class TokenConfig:
    """토큰 설정 관리 클래스"""
    JWT_SECRET_KEY = settings.jwt_secret_key
    ALGORITHM = settings.jwt_algorithm
class TokenService:
    """토큰 발급/검증 관련 로직"""
    def __init__(self):
        self.jwt_secret_key = settings.jwt_secret_key
        self.algorithm = settings.jwt_algorithm

    def create_access_token(self,member: Member) -> str:
        """액세스 토큰 생성

            Args:
                user: 사용자 정보

            Returns:
                str: JWT 액세스 토큰
        """
        # JWT는 3개 파트로 구성된 문자열 -> header.payload.signature
        jwt_payload = {
             # sub: subject의 약자로 이 토큰이 누구에 대한 것인지 나타내는 고유 식별자임
             # exp : 토큰의 만료 시간
            "sub": str(member.member_seq),
            "exp": datetime.now(UTC) + timedelta(hours=1)
        }
        return jwt.encode(
            jwt_payload,
            self.jwt_secret_key,
            algorithm=self.algorithm
        )
    # TODO : 리프레시 토큰 생성  -> 추후 추가 예정
    def create_refresh_token(self, member: Member) -> str:
        return jwt.encode(
            {
                "sub": str(member.member_seq),
                "exp": datetime.now(UTC) + timedelta(days=365 * 10)
            },
            self.jwt_secret_key,
            algorithm=self.algorithm
        )
