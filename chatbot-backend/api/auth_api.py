# 🔹 auth는 "인증/인가" 처리
#로그인 관련 API (일반 / 소셜 로그인)

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.openapi.docs import get_swagger_ui_html
from schemas.auth import LoginRequestDto, LoginResponseDto, RegisterRequestDto
from services.auth_service import auth_service
from db.session import get_session

router = APIRouter(prefix="/auth")


@router.post("/login", response_model=LoginResponseDto,
    summary="이메일 로그인",
    description="이메일 로그인 API"
)
def email_login(request: LoginRequestDto, db: Session = Depends(get_session)):
    return auth_service.login(request, db)

# TODO : 로그아웃 추가 예정 /api/auth/logout - 쿠키, 토큰 등 관리 어케하지
@router.post("/logout")
def logout():
    return auth_service.logout()



    
# 이후 토큰 발급, 인증 확인 등 추가 예정
