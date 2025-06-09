from sqlalchemy.orm import Session
from models import Emotion  # SQLModel 테이블
from typing import Optional

def get_emotion_by_seq(db: Session, emotion_seq: int) -> Optional[Emotion]:
    return db.query(Emotion).filter(Emotion.emotion_seq == emotion_seq).first()
