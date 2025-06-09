from sqlalchemy.orm import Session
from models import Emotion

def get_emotion_by_seq(db: Session, emotion_seq: int) -> Emotion | None:
    return db.query(Emotion).filter(Emotion.emotion_seq == emotion_seq).first()
