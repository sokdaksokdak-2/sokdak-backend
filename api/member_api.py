# 회원 등록, 조회, 수정 등 회원 관련 API
from fastapi import APIRouter, Depends, status, HTTPException, Query
from fastapi.responses import Response
from starlette.status import HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND
from schemas.member import RegisterRequestDto, UpdateNicknameRequestDto
from services import MemberService
from sqlalchemy.orm import Session
from db.session import get_session
from datetime import date
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

def get_member_service(db: Session = Depends(get_session)) -> MemberService:
    return MemberService(db)


# 🚩회원 관련 API

@router.post("/register", status_code=status.HTTP_201_CREATED,
    summary="회원가입",
    description="회원가입 API"
)
def register_member(request: RegisterRequestDto, 
                    member_service: MemberService = Depends(get_member_service)
                    ):
    return member_service.register(request)

# 닉네임 변경
@router.put("/nickname",
            status_code=status.HTTP_200_OK,
            summary="닉네임 변경 API",
            description="회원가입, 회원정보 수정 시 닉네임 설정 및 변경"
            )
def update_member_nickname(request: UpdateNicknameRequestDto, 
                           member_service: MemberService = Depends(get_member_service)):
    return member_service.update_nickname(request)

@router.delete("/{member_seq}",
               status_code=status.HTTP_200_OK,
               summary="회원 탈퇴 API",
               description="회원 탈퇴 및 소셜 연동 정보 삭제 API"
               )
def delete_member_account(member_seq: int, member_service: MemberService = Depends(get_member_service)):
    return member_service.delete_member(member_seq)

