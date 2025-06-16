from sqlalchemy.orm import Session
from fastapi import HTTPException
from crud.emo_report import (
    get_emotion_report, save_emotion_report,
    get_monthly_emotion_stats, get_monthly_contexts
)
from models.emotion_report import EmotionReport
from datetime import date, timedelta, datetime
from utils import calculate_emotion_distribution
from services import generate_monthly_summary

def create_emotion_report(db: Session, member_seq: int, report_month: date) -> EmotionReport:
    """
    월간 감정 리포트 생성(또는 이미 있으면 반환)
    - report_month (예: 2025-06-01)로 리포트가 있는지 조회하고,
    - 실제 오늘 날짜까지의 데이터로 리포트 계산
    - 이미 리포트가 있더라도, emotion_distribution이 비어있으면 새로 계산하여 덮어씀
    """
    # 1. 이미 리포트가 있는지 확인
    existing = get_emotion_report(db, member_seq, report_month)

    current_actual_date = date.today()

    # 해당 월의 1일부터 오늘까지로 기간 설정
    start_date = report_month.replace(day=1)
    end_of_requested_month = (start_date + timedelta(days=32)).replace(day=1) - timedelta(days=1)

    if report_month.year == current_actual_date.year and report_month.month == current_actual_date.month:
        end_date = current_actual_date
    else:
        end_date = end_of_requested_month

    # 2. 감정 raw 데이터 쿼리 → 비율 계산
    stats = get_monthly_emotion_stats(db, member_seq, start_date, end_date)
    print(f"DEBUG: start_date={start_date}, end_date={end_date}")
    print(f"DEBUG: member_seq={member_seq}")
    print(f"DEBUG: Raw stats from DB: {stats}")
    
    raw_emotion_distribution = calculate_emotion_distribution(stats)
    print(f"DEBUG: Calculated raw_emotion_distribution: {raw_emotion_distribution}") # <--- 이 부분도 확인!

    # 3. 감정 기록이 하나도 없으면 404 에러 발생
    if not raw_emotion_distribution:
        # 기존 리포트가 있고 빈 리포트라면 삭제 후 404 반환
        if existing and not existing.emotion_distribution:
            # 여기서는 빈 리포트를 삭제하는 로직을 추가할 수 있지만, 현재는 단순히 404 반환
            pass # DB에서 빈 리포트를 삭제하는 로직은 crud에 추가해야 함
        print(f"DEBUG: No raw_emotion_distribution found for member_seq={member_seq}, month={report_month}. Raising 404.")
        raise HTTPException(status_code=404, detail="이 달의 감정 기록이 없습니다.")

    # 4. emotion_distribution 최종 계산 (5가지 감정 모두 포함)
    all_emotion_seqs = [1, 2, 3, 4, 5] # 가정: 5가지 감정의 emotion_seq가 1부터 5까지라고 가정
    emotion_distribution = {seq: 0.0 for seq in all_emotion_seqs}

    for seq, ratio in raw_emotion_distribution.items():
        emotion_distribution[seq] = ratio

    # 5. DB 저장 또는 업데이트
    if existing:
        # 기존 리포트 업데이트
        existing.emotion_distribution = emotion_distribution
        existing.created_at = datetime.now() # 업데이트 시각 갱신
        report = save_emotion_report(db, existing)
    else:
        # 새 리포트 생성
        report = EmotionReport(
            member_seq=member_seq,
            report_date=start_date,
            emotion_distribution=emotion_distribution,
        )
        report = save_emotion_report(db, report)

    return report

