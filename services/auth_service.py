# service/auth_service.py
# 로그인, 로그아웃, 토큰 재발급

from fastapi import HTTPException
from sqlalchemy.orm import Session
from schemas.auth import LoginRequestDto, LoginResponseDto
from passlib.context import CryptContext
from crud import member as member_crud
from core.token import TokenService

class AuthConfig:
    """인증 관련 설정"""
    PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")


# TODO : 추후 예외처리 확장 필요

class AuthService:
    """인증 관련 서비스를 처리하는 클래스"""

    def __init__(self, db: Session) :
        self.db = db
        self.pwd_context = AuthConfig.PWD_CONTEXT
        self.token_service = TokenService()


    def get_password_hash(self, password: str) -> str:
        """비밀번호 해시화
        
        Args:
            password: 평문 비밀번호
            
        Returns:
            str: 해시된 비밀번호
        """
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """비밀번호 검증
        
        Args:
            plain_password: 평문 비밀번호
            hashed_password: 해시된 비밀번호
            
        Returns:
            bool: 비밀번호 일치 여부
        """
        return self.pwd_context.verify(plain_password, hashed_password)

    def login(self, request: LoginRequestDto) -> LoginResponseDto:
        """로그인 처리
        
        Args:
            request: 로그인 요청 DTO
            db: 데이터베이스 세션
            
        Returns:
            LoginResponseDto: 로그인 응답 DTO
            
        Raises:
            HTTPException: 인증 실패시 발생
        """
        member = member_crud.get_member_by_email(self.db, request.email)

        if not member:
            raise HTTPException(status_code=404, detail="존재하지 않는 이메일")

        if not member.password or not self.verify_password(request.password, member.password):
            raise HTTPException(status_code=401, detail="잘못된 비밀번호")
        
        return LoginResponseDto(
            access_token=self.token_service.create_access_token(member),
            refresh_token=self.token_service.create_refresh_token(member),
            member_seq=member.member_seq,
            nickname=member.nickname,
            # character_name=member.character_name
        )

