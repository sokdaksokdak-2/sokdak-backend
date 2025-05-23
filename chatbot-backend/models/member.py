from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, UTC


class Member(SQLModel, table=True):
    __tablename__ = "member"
    
    member_seq: Optional[int] = Field(default=None, primary_key=True)
    nickname: str = Field(max_length=100, nullable=False, description="닉네임")
    email: str = Field(max_length=255, nullable=False, unique=True, description="이메일")
    password: Optional[str] = Field(default=None, max_length=255, description="비밀번호")
    joined_at: datetime = Field(default_factory=lambda: datetime.now(UTC), description="가입일")
    profile_url: Optional[str] = Field(default=None, max_length=255, description="프로필 URL")
