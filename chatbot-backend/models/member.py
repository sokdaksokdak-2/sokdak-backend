from typing import Optional
from sqlmodel import SQLModel, Field, Enum
import enum
from datetime import datetime

class LoginType(str, enum.Enum):
    normal = "normal"
    kakao = "kakao"
    google = "google"
    naver = "naver"

class Member(SQLModel, table=True):
    __tablename__ = "member"
    
    member_seq: Optional[int] = Field(default=None, primary_key=True)
    nickname: str
    email: str
    password: Optional[str] = None
    login_type: LoginType = LoginType.normal
    oauth_provider: Optional[str] = None
    oauth_id: Optional[str] = None
    email_verified: bool = False
    last_login_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
