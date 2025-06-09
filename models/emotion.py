from typing import Optional
from sqlmodel import SQLModel, Field

class Emotion(SQLModel, table=True):
    __tablename__ = "emotion"

    emotion_seq: Optional[int] = Field(default=None, primary_key=True)
    name_kr: str = Field(max_length=30, nullable=False, unique=True)
    name_en: str = Field(max_length=30, nullable=False, unique=True)
    color_code: Optional[str] = Field(default=None, max_length=7)
    
    # details: List["EmotionDetail"] = Relationship(back_populates="emotion")