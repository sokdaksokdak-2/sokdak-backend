from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date
 
class EmotionCalendar(SQLModel, table=True):
    __tablename__ = "emotion_calendar"
 
    # 앱 단위에서 중복 체크 - calendar_date, member_seq
    # 저장 전에 calendar_date + member_seq로 먼저 조회해서 존재 여부 체크
    # 존재하면 덮어쓰기 or 예외 처리
    # Optional[int] : 타입 힌트
 
    calendar_seq: Optional[int] = Field(default=None, primary_key=True)
    calendar_date: date = Field(nullable=False)
   
 
    # 외래키 - 제약조건 X
    member_seq: int = Field(nullable=False)
 