# 회원가입, 회원정보 조회/수정 등

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from schemas import RegisterRequestDto, UpdateNicknameRequestDto
from sqlalchemy.orm import Session
from crud import member as member_crud
from crud import member_oauth as member_oauth_crud
from passlib.context import CryptContext
from sqlalchemy.exc import SQLAlchemyError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class MemberService:
    def __init__(self, db: Session):
        self.db = db
    # 회원가입 - 시작하기 누를 시 커밋됨, 닉네임, 캐릭터이름 등은 수정 api를 이용해 디폴트에서 변경
    # 닉네임은 기본값으로 email 주소 사용
    def register(self, request: RegisterRequestDto):
        existing_user = member_crud.get_member_by_email(self.db, request.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="이미 존재하는 이메일입니다.")
        # 비밀번호 암호화
        hashed_password = pwd_context.hash(request.password)
        member_crud.register_member(
            self.db,
            request.email, 
            hashed_password, 
        )
        
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message" : "회원가입 성공"})

    # 캐릭터 이름 변경 [❌ 사용 중지된 API입니다. - 2025.06.02]
    # def update_character_name(self, request: UpdateCharacterNameRequestDto):
    #     member = member_crud.get_member_by_member_seq(self.db, request.member_seq)
    #     if not member : 
    #         raise HTTPException(status_code=404, detail="존재하지 않는 회원입니다.")
        
    #     member_crud.update_character_name(self.db, member, request.character_name)
        
    #     return JSONResponse(status_code=status.HTTP_200_OK, content={"message" : "캐릭터 이름 변경 성공"})
    
    # 닉네임 변경
    def update_nickname(self, request: UpdateNicknameRequestDto):
        member = member_crud.get_member_by_member_seq(self.db, request.member_seq)
        if not member : 
            raise HTTPException(status_code=404, detail="존재하지 않는 회원입니다.")
        member_crud.update_nickname(self.db,member, request.nickname)
        
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message" : "닉네임 변경 성공"})
    
    # TODO : 회원 탈퇴
    def delete_member(self, member_seq: int):
        try:
            delete_count_member = member_crud.delete_member_by_member_seq(self.db, member_seq)
            delete_count_oauth = member_oauth_crud.delete_oauth_account_by_member_seq(self.db, member_seq)

            # 회원 자체 삭제 실패 시 예외 발생
            if delete_count_member == 0:
                raise HTTPException(status_code=404, detail="회원 정보를 찾을 수 없습니다.")

            # 소셜 연동 정보는 없을 수도 있으므로 경고 로그만
            if delete_count_oauth == 0:
                print(f"⚠️ 소셜 연동 정보 없음: member_seq={member_seq}")

            self.db.commit()

        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail="회원 탈퇴 중 DB 오류 발생: " + str(e))
