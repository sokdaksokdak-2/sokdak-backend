from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_session
from schemas import EmotionReportResponse
from services.emo_report_service import create_emotion_report
from pydantic import BaseModel
from datetime import date

router = APIRouter()

# 요청 바디용 Pydantic 모델
class EmotionReportRequest(BaseModel):
    year: int
    month: int
    member_seq: int

# 월간 감정 리포트 생성 및 조회 (POST)
@router.post("/", response_model=EmotionReportResponse)
def create_or_read_emotion_report(
    req: EmotionReportRequest,
    db: Session = Depends(get_session)
):
    """
    월간 감정 리포트 생성 및 조회 API (POST)
    - year, month, member_seq를 body로 받음
    - 해당 월의 리포트가 없으면 캘린더 테이블에서 데이터 계산 후 생성
    - 있으면 바로 반환
    - 반환: EmotionReportResponse
    """
    try:
        report_month = date(req.year, req.month, 1)
    except ValueError:
        raise HTTPException(status_code=400, detail="유효하지 않은 연도 또는 월입니다.")

    # 리포트 생성(또는 이미 있으면 반환)
    report = create_emotion_report(db, req.member_seq, report_month)
    if not report:
        raise HTTPException(status_code=404, detail="이 달의 리포트가 존재하지 않습니다.")
    return report