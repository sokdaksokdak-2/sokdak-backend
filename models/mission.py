from sqlmodel import SQLModel, Field
from typing import Optional

class Mission(SQLModel, table=True):
    __tablename__ = "mission"
    
    mission_seq: Optional[int] = Field(default=None, primary_key=True)
    content: str = Field(nullable=False, description="미션 내용")

    # 외래키 - 제약조건 X
    emotion_seq: int = Field(nullable=False, description="감정 종류") # 외래키

