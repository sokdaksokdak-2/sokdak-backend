from pydantic import BaseModel
from datetime import date
from typing import Optional

class EmotionCalendarSummaryResponse(BaseModel):
    calendar_date: date
    character_image_url: str

class EmotionCalendarResponse(BaseModel):
    character_image_url: str
    context: Optional[str]
    calendar_date: date

    


class EmotionCalendarUpdateRequest(BaseModel): # memo삭제
    character_image_url: Optional[str] = None
    context: Optional[str] = None
    title: Optional[str] = None
    emotion_seq: Optional[int] = None  # 감정 변경을 위한 필드



class EmotionCalendarCreateRequest(BaseModel): 
    member_seq: int
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
