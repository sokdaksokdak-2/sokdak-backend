from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from db.session import get_session
from schemas import EmotionReportResponse
from crud import create_emotion_report, get_emotion_report
from datetime import date

router = APIRouter()

@router.post("/", response_model=EmotionReportResponse)
def generate_report(
    today: date,
    member_seq: int,  # 실제 구현에서는 JWT에서 가져오는 것이 일반적
    db: Session = Depends(get_session)
):
    """
    월별 감정 요약 리포트를 생성합니다. (매월 1일 실행)
    - 감정 비율 (파이차트용 JSON)
    - GPT를 활용한 텍스트 요약
    """
    report = create_emotion_report(db, member_seq, today)
    return report

@router.get("/", response_model=EmotionReportResponse)
def read_emotion_report(
    year: int = Query(..., ge=2000, le=2100, description="조회할 연도"),
    month: int = Query(..., ge=1, le=12, description="조회할 월"),
    member_seq: int = Query(..., description="회원 시퀀스"),
    db: Session = Depends(get_session)
):
    try:
        report_month = date(year, month, 1)
    except ValueError:
        raise HTTPException(status_code=400, detail="유효하지 않은 연도 또는 월입니다.")

    report = get_emotion_report(db, member_seq, report_month)

    if not report:
        raise HTTPException(status_code=404, detail="이 달의 리포트가 존재하지 않습니다.")

    return report
