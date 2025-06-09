from sqlmodel import SQLModel, Field
from typing import Optional
from enum import Enum

class OAuthProvider(str, Enum):
    KAKAO = "kakao"
    GOOGLE = "google"
    NAVER = "naver"

class MemberOAuth(SQLModel, table=True):
    __tablename__ = "member_oauth"
    
    oauth_seq: Optional[int] = Field(default=None, primary_key=True)
    provider: OAuthProvider = Field(nullable=False, description="kakao | google | naver")  # 소셜 제공자
    oauth_id: str = Field(max_length=255, nullable=False) # 소셜 고유 ID
    # 외래키 - 제약조건 X
    member_seq: int = Field(nullable=False) # 연결된 내부 회원 ID
