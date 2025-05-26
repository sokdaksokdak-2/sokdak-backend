# Pydantic 모듈은 데이터 유효성 검사, 데이터 변환, 모델 시퀀싱 등을 지원하는 모듈
# Python 클래스 BaseModel을 상속받은 클래스로 이 클래스는 입력값을 검증하고, 자동을 타입 변환도 해줌
from pydantic import BaseModel, EmailStr
from typing import Optional

class LoginRequestDto(BaseModel):
    email: EmailStr
    password: str

# TODO 로그인 뭘 응답을....? cookie 설정해야하지않나?
class LoginResponseDto(BaseModel): 
    member_seq: int
    nickname: str
    character_name:str

# TODO : 소셜 로그인 추가
# class OAuthLoginDTO(BaseModel):
#     provider: Literal["kakao", "google", "naver"]
#     oauth_id: str
#     email: Optional[str]
#     nickname: Optional[str]
