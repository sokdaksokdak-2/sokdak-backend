from pydantic import BaseModel

class EmotionDto(BaseModel):
    emotion_seq: int
    name_kr: str
    color_code: str
    character_image_url: str
    emotion_description: str