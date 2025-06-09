from sqlalchemy.orm import Session
from models.emotion_detail import EmotionDetail


def get_emotion_detail_by_emotion_detail_seq(db: Session, emotion_detail_seq: int) -> EmotionDetail:
    return (
        db.query(EmotionDetail)
        .filter(EmotionDetail.emotion_detail_seq == emotion_detail_seq)
        .first()
    )