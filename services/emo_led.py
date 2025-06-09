from crud import get_emotion_by_seq
from sqlalchemy.orm import Session

def get_color_for_emotion(db: Session, emotion_seq: int) -> str:
    emotion = get_emotion_by_seq(db, emotion_seq)
    if not emotion:
        raise ValueError("해당 감정을 찾을 수 없습니다.")
    return emotion.color_code

