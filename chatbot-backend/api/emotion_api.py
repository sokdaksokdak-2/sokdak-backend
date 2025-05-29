from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_session
from crud.emotion import create_emotion

router = APIRouter(prefix="/emotion")

@router.post("/test-create-emotion")
def test_create_emotion(
    name_kr: str,
    name_en: str,
    color_code: str = None,
    character_image_url: str = None,
    db: Session = Depends(get_session)
):
    emotion = create_emotion(db, name_kr, name_en, color_code, character_image_url)
    return {
        "emotion_seq": emotion.emotion_seq,
        "name_kr": emotion.name_kr,
        "name_en": emotion.name_en,
        "color_code": emotion.color_code,
        "character_image_url": emotion.character_image_url
    }
