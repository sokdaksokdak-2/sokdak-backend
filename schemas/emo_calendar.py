from pydantic import BaseModel
from datetime import date
from typing import Optional

class EmotionCalendarSummaryResponse(BaseModel):
    calendar_date: date
    emotion_seq: Optional[int]

class EmotionCalendarResponse(BaseModel):
    emotion_seq: Optional[int]
    context: Optional[str]
    calendar_date: date
    
    class Config:
        orm_mode = True


class EmotionCalendarUpdateRequest(BaseModel): 
    context: Optional[str] = None
    title: Optional[str] = None
    emotion_seq: Optional[int] = None  # 감정 변경을 위한 필드


class EmotionCalendarCreateRequest(BaseModel): # 추가
    member_seq: int  # ✅ 추가
    calendar_date: date
    title: str
    context: str
    emotion_seq: int

class EmotionCalendarFromTextRequest(BaseModel):
    member_seq: int
    calendar_date: date
    text: str
    title: Optional[str] = None

### 추가
class CalendarCreateResponse(BaseModel):
    calendar_seq: int
    calendar_date: date
    member_seq: int
    title: str
    context: str
    emotion_seq: int

