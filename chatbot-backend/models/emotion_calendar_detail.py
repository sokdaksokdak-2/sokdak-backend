from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, UTC
from enum import Enum
from sqlalchemy import Text, Column


class SourceType(str, Enum):
    USER = "user"
    AI = "ai"

class EmotionCalendarDetail(SQLModel, table=True):
    __tablename__ = "emotion_calendar_details"

    detail_seq: Optional[int] = Field(default=None, primary_key=True)
    emotion_score: int = Field(default=1)
    source: SourceType = Field(default=SourceType.USER, nullable=False, description="user | ai") # 기본값 user라고 설정
    context: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    title: str = Field()

    # 외래키 - 제약조건X 정수필드
    calendar_seq: int = Field()
    emotion_seq: int = Field()
