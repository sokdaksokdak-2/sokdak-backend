# service/auth_service.py
# 로그인, 로그아웃, 토큰 재발급

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from models import Member  # SQLModel 아님 (ORM BaseModel이라면)
from schemas.auth import LoginRequestDto, LoginResponseDto, RegisterRequestDto
# TODO requirements.txt 추가 pip install passlib[bcrypt]
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:

    # 비밀번호 검증
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    # 로그인
    def login(self, request: LoginRequestDto, db: Session) -> LoginResponseDto:
        user = db.query(Member).filter(Member.email == request.email).first()
        if not user:
            raise HTTPException(status_code=404, detail="존재하지 않는 이메일입니다.")
        # if not user.password or not pwd_context.verify(request.password, user.password):
        # TODO : 비밀번호 암호화 추가 후 수정
        if not user.password == request.password :
            raise HTTPException(status_code=401, detail="비밀번호가 틀렸습니다.")
        
        return LoginResponseDto(
            member_seq=user.member_seq,
            nickname=user.nickname,
            character_name=user.character_name
        )

    def logout(self):
        # 토큰 기반이라면 클라이언트에서 삭제 or 블랙리스트 방식
        return {"message" : "로그아웃 처리됨"}



# 인스턴스 생성
auth_service = AuthService()

