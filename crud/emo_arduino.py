from sqlalchemy.orm import Session
from models import Emotion  # 감정 테이블 모델

def get_emotion_by_seq(db: Session, emotion_seq: int) -> Emotion:
    return db.query(Emotion).filter(Emotion.emotion_seq == emotion_seq).first()
