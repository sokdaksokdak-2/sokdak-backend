# 🔹 auth는 "인증/인가" 처리
# 일반 로그인 API

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.auth import LoginRequestDto, LoginResponseDto
from services import AuthService
from db.session import get_session


router = APIRouter()

# DI 주입 방식으로 변경
# TODO : 이후 dependencies/auth_dependencies.py 파일로 분리
def get_auth_service(db: Session = Depends(get_session)) -> AuthService:
    return AuthService(db)


@router.post("/login/local", 
    response_model=LoginResponseDto,
    dependencies=[Depends(get_auth_service)],
    responses={
        404: {"description": "존재하지 않는 이메일"},
        401: {"description": "비밀번호 불일치"}
    },
    response_model_include={"access_token","refresh_token","member_seq", "nickname", "email"},
    summary="이메일 로그인",
    description="이메일 로그인 API"
)
def email_login(request: LoginRequestDto, auth_service: AuthService = Depends(get_auth_service)):
    return auth_service.login(request)


# 이후 토큰 발급, 인증 확인 등 추가...?




