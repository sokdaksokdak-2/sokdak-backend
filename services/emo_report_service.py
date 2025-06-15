from sqlalchemy.orm import Session
from fastapi import HTTPException
from crud.emo_report import (
    get_emotion_report, save_emotion_report,
    get_monthly_emotion_stats, get_monthly_contexts
)
from models.emotion_report import EmotionReport
from datetime import date, timedelta
from utils import calculate_emotion_distribution
from services import generate_monthly_summary

def create_emotion_report(db: Session, member_seq: int, today: date) -> EmotionReport:
    """
    월간 감정 리포트 생성(또는 이미 있으면 반환)
    - 해당 월의 1일부터 today까지의 데이터로 계산
    """
    # 이미 리포트가 있으면 반환
    existing = get_emotion_report(db, member_seq, today)
    if existing:
        return existing

    # 해당 월의 1일부터 today까지로 기간 설정
    start_date = today.replace(day=1)
    end_date = today

    # 1. 감정 raw 데이터 쿼리 → 비율 계산
    stats = get_monthly_emotion_stats(db, member_seq, start_date, end_date)
    emotion_distribution = calculate_emotion_distribution(stats)

    if not emotion_distribution:
        # 감정 기록이 하나도 없으면 예외 발생
        raise HTTPException(status_code=404, detail="이 달의 감정 기록이 없습니다.")

    # 2. 감정 메모 context 쿼리 (주석 처리)
    # context_texts = get_monthly_contexts(db, member_seq, start_date, end_date)

    # 3. GPT 요약 (주석 처리)
    # summary_text = generate_monthly_summary(context_texts) if context_texts else None

    # 4. DB 저장
    report = EmotionReport(
        member_seq=member_seq,
        report_date=start_date,
        emotion_distribution=emotion_distribution,
        # summary_text=summary_text
    )

    stats = get_monthly_emotion_stats(db, member_seq, start_date, end_date)
    print("DEBUG stats:", stats)
    return save_emotion_report(db, report)

