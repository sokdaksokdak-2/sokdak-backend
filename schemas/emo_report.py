from typing import Optional, Dict
from datetime import date, datetime
from pydantic import BaseModel

# 클라이언트에게 보여줄 감정 리포트 응답 스키마
class EmotionReportResponse(BaseModel):
    report_date: date  # 예: 2025-05-01 (5월 리포트)
    emotion_distribution: Dict[str, float]  # 감정별 비율
    summary_text: Optional[str] = None
    created_at: datetime

    class Config:
        orm_mode = True  # SQLModel -> Pydantic 자동 변환 허용
