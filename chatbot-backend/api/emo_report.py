from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from db.session import get_session
from schemas import EmotionReportResponse
from services.emo_report_service import create_emotion_report
from crud.emo_report import get_emotion_report
from datetime import date

router = APIRouter()

# 월간 감정 리포트 조회
@router.get("/", response_model=EmotionReportResponse)
def read_emotion_report(
    year: int = Query(..., ge=2000, le=2100, description="조회할 연도"),
    month: int = Query(..., ge=1, le=12, description="조회할 월"),
    member_seq: int = Query(..., description="회원 시퀀스"),
    db: Session = Depends(get_session)
):
    """
    월간 감정 리포트 조회 API
    - year, month: 조회할 연/월
    - member_seq: 회원 시퀀스
    - 반환: EmotionReportResponse
    - 리포트가 없으면 404 에러 반환
    """
    try:
        report_month = date(year, month, 1)
    except ValueError:
        raise HTTPException(status_code=400, detail="유효하지 않은 연도 또는 월입니다.")

    report = get_emotion_report(db, member_seq, report_month)
    if not report:
        raise HTTPException(status_code=404, detail="이 달의 리포트가 존재하지 않습니다.")
    return report