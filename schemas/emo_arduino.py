from pydantic import BaseModel

class EmotionChangeRequest(BaseModel):
    member_seq: int
    current_emotion_seq: int
