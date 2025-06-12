from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class EmotionCalendarSummaryResponse(BaseModel):
    calendar_date: date
    emotion_seq: Optional[int]

class EmotionCalendarResponse(BaseModel):
    detail_seq: int
    emotion_seq: int
    title: str
    context: str
    calendar_date: date

    class Config:
        orm_mode = True


class EmotionCalendarUpdateRequest(BaseModel):
    emotion_seq: int | None = Field(None, ge=1, le=5)   # 1‒5 중 선택
    title: str | None = None
    context: str | None = None                          # 메모(내용)

    class Config:
        orm_mode = True


class EmotionCalendarCreateRequest(BaseModel): # 추가
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

