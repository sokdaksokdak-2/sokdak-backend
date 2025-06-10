from typing import Optional
from sqlmodel import SQLModel, Field
from sqlalchemy import UniqueConstraint

class EmotionDetail(SQLModel, table=True):
    __tablename__ = "emotion_details"

    emotion_detail_seq: Optional[int] = Field(default=None, primary_key=True)
    emotion_score: int = Field(nullable=False, ge=1, le=3)  # 강도 1~3 범위 제한
    character_image_url: str = Field(max_length=255, nullable=True) # TODO : 추후 확장 시

    emotion_seq: int = Field(nullable=False)

    # emotion_seq: int = Field(foreign_key="emotion.emotion_seq", nullable=False)
    # emotion: Optional["Emotion"] = Relationship(back_populates="details")

    __table_args__ = (
        UniqueConstraint("emotion_seq", "emotion_score"),  # 감정+강도 조합 유일하게 보장
    )

