from pydantic import BaseModel
from schemas.emotion import EmotionDto
from datetime import datetime
import json


class ChatRequestDto(BaseModel):
    member_seq: int
    user_message: str

class ChatResponseDto(BaseModel):
    chatbot_response: str
    emotion_seq: int
    emotion_score: int
    # color_code : str = "#000000"  # 또는 적절한 기본 색상

class EmotionAnalysisResponseDto(BaseModel):
    emotion_seq: int
    strength: int

class StreamingChatRequestDto(BaseModel):
    user_message: str
    member_seq: int   # 추가 필드!
    
class StreamingChatResponseDto(BaseModel):
    message: str
    emotion: EmotionDto
    media_type: str

class ChatHistoryDto(BaseModel):
    user_message: str
    chatbot_response: dict
    # emotion_seq: int
    # emotion_score: int
    created_at: datetime
    # character_name: str | None = None