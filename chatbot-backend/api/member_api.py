# 회원 등록, 조회, 수정 등 회원 관련 API
from fastapi import APIRouter, Depends, status
from schemas.member import RegisterRequestDto, UpdateCharacterNameRequestDto, UpdateNicknameRequestDto
from services.member_service import MemberService
from sqlalchemy.orm import Session
from db.session import get_session

router = APIRouter(prefix="/member")


# TODO Response 모델 추가
@router.post("/register", status_code=status.HTTP_201_CREATED,
    summary="회원가입",
    description="회원가입 API"
)
def register(request: RegisterRequestDto, db: Session = Depends(get_session)):
    member_service = MemberService(db)
    return member_service.register(request)

# 캐릭터 이름 수정
@router.put("/update/character-name",
            status_code=status.HTTP_200_OK,
            summary="캐릭터 이름 변경 API",
            description="회원가입, 회원정보 수정 시 캐릭터 이름 설정 및 변경"
            )
def update_character_name(request: UpdateCharacterNameRequestDto, db: Session=Depends(get_session)):
    member_service = MemberService(db)
    return member_service.update_character_name(request)

# 닉네임 변경
@router.put("/update/nickname",
            status_code=status.HTTP_200_OK,
            summary="닉네임 변경 API",
            description="회원가입, 회원정보 수정 시 닉네임 설정 및 변경"
            )
def update_nickname(request: UpdateNicknameRequestDto, db: Session=Depends(get_session)):
    member_service = MemberService(db)
    return member_service.update_nickname(request)