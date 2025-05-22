from typing import Optional
from sqlmodel import SQLModel, Field

class Emotion(SQLModel, table=True):
    __tablename__ = "emotion"

    emotion_seq: Optional[int] = Field(default=None, primary_key=True)
    name_kr: str
    name_en: str
    color_code: Optional[str] = None  # HEX 코드 (#FF5733)
    character_image_url: Optional[str] = None
