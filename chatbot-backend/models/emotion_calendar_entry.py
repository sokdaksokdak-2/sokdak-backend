from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
import enum
from models.member import Member
from models.emotion import Emotion

class SourceType(str, enum.Enum):
    ai = "ai"
    user = "user"

class EmotionCalendarEntry(SQLModel, table=True):
    __tablename__ = "emotion_calendar_entry"
    
    entry_seq: Optional[int] = Field(default=None, primary_key=True)
    source: SourceType
    memo: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    member_seq: int = Field(foreign_key="member.member_seq")
    emotion_seq: int = Field(foreign_key="emotion.emotion_seq")

    member: Optional[Member] = Relationship()
    emotion: Optional[Emotion] = Relationship()
