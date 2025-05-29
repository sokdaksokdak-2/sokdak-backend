# 🔹 auth는 "인증/인가" 처리
# 일반 로그인 API

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.auth import LoginRequestDto, LoginResponseDto
from services.auth_service import AuthService
from db.session import get_session


router = APIRouter(prefix="/auth")

# DI 주입 방식으로 변경
# TODO : 이후 dependencies/auth_dependencies.py 파일로 분리
def get_auth_service(db: Session = Depends(get_session)) -> AuthService:
    return AuthService(db)


# TODO : 소셜로그인과 동일한 응답, 이후 쿠키에 저장할 내용 다시 확인
@router.post("/login/local", 
    response_model=LoginResponseDto,
    dependencies=[Depends(get_auth_service)],
    responses={
        404: {"description": "존재하지 않는 이메일"},
        401: {"description": "비밀번호 불일치"}
    },
    response_model_include={"access_token","refresh_token","member_seq", "nickname", "character_name"},
    summary="이메일 로그인",
    description="이메일 로그인 API"
)
def email_login(request: LoginRequestDto, auth_service: AuthService = Depends(get_auth_service)):
    return auth_service.login(request)

# TODO : 로그아웃은 프론트에 맡김 - 쿠키, 토큰 등 관리 어케하지


# 이후 토큰 발급, 인증 확인 등 추가...?




