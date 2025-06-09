from pydantic import BaseModel

class EmotionRequest(BaseModel):
    emotion_seq: int  # 예: 1 = 기쁨(강도1)

class EmotionResponse(BaseModel):
    color_code: str
