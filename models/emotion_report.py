from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import date, datetime
from sqlalchemy import Column
from sqlalchemy.dialects.sqlite import JSON

class EmotionReport(SQLModel, table=True):
    __tablename__ = "emotion_report"

    report_id: int = Field(primary_key=True)
    report_date: date = Field(nullable=False, description="해당 리포트가 속한 월 (예: 2025-05-01)")
    summary_text: Optional[str] = Field(default=None)
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    member_seq: int = Field(nullable=False, description="회원 시퀀스")

# JSON 타입 명시
    emotion_distribution: Optional[dict] = Field(
        default=None,
        sa_column=Column(JSON),
        description='(예: { "1": 0.4, "2": 0.2, ... }) / emotion_seq별 비율'
    )