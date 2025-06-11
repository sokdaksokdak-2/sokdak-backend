# Pydantic 모듈은 데이터 유효성 검사, 데이터 변환, 모델 시퀀싱 등을 지원하는 모듈
# Python 클래스 BaseModel을 상속받은 클래스로 이 클래스는 입력값을 검증하고, 자동을 타입 변환도 해줌
from pydantic import BaseModel, EmailStr

class LoginRequestDto(BaseModel):
    email: EmailStr
    password: str

# cookie 설정해야하지않나?
# 로그인 후 토큰정보, 사용자 정보
class LoginResponseDto(BaseModel): 
    access_token: str
    refresh_token: str
    member_seq: int
    nickname: str
    email: str

