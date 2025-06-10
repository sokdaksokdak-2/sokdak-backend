from sqlalchemy.orm import Session
from models.emotion import Emotion
from sqlmodel import select

def get_emotion_by_emotion_seq(db: Session, emotion_seq: int) -> Emotion:
    return db.query(Emotion).filter(Emotion.emotion_seq == emotion_seq).first()
