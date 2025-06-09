from pydantic import BaseModel, EmailStr

# TODO 회원가입은 
class RegisterRequestDto(BaseModel):
    email: EmailStr
    password: str

class UpdateCharacterNameRequestDto(BaseModel):
    member_seq: int
    character_name: str

class UpdateNicknameRequestDto(BaseModel):
    member_seq: int
    nickname: str