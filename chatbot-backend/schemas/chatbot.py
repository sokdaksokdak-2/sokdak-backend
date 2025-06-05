from pydantic import BaseModel
from schemas.emotion import EmotionDto

class StreamingChatRequestDto(BaseModel):
    user_message: str
    member_seq: int   # 추가 필드!
    
class StreamingChatResponseDto(BaseModel):
    message: str
    emotion: EmotionDto
    media_type: str
