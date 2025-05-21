from sqlalchemy.ext.asyncio import AsyncSession
from models.emotion import Emotion

def create_emotion(db: AsyncSession, name_kr: str, name_en: str, color_code: str = None, character_image_url: str = None) -> Emotion:
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
