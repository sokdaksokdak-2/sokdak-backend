from sqlalchemy.orm import Session
from models.emotion import Emotion
from sqlmodel import select

def create_emotion(db: Session, name_kr: str, name_en: str, color_code: str = None, character_image_url: str = None) -> Emotion:
    new_emotion = Emotion(
        name_kr=name_kr,
        name_en=name_en,
        color_code=color_code,
        character_image_url=character_image_url
    )
    db.add(new_emotion)
    db.commit()
    db.refresh(new_emotion)
    return new_emotion

def get_emotion_by_emotion_seq(db: Session, emotion_seq: int) -> Emotion:
    return db.query(Emotion).filter(Emotion.emotion_seq == emotion_seq).first()

async def get_color_by_emotion_seq(db: Session, emotion_seq: int) -> str:
    color_code = db.query(Emotion.color_code).filter(Emotion.emotion_seq == emotion_seq).scalar()
    return color_code or "#FFFFFF"