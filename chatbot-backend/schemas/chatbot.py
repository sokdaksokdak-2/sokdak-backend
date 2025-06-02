from pydantic import BaseModel
from schemas.emotion import EmotionDto

class StreamingChatRequestDto(BaseModel):
    user_message: str

class StreamingChatResponseDto(BaseModel):
    message: str
    emotion: EmotionDto
    media_type: str
