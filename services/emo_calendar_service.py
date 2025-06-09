from sqlalchemy.orm import Session
from crud.emo_calendar import (
    get_strongest_emotions_by_month, get_emotions_by_date,
    update_emotion_calendar, create_emotion_calendar, delete_emotion_calendar,
    get_monthly_emotion_stats, get_monthly_contexts, save_emotion_from_text
)
from utils.emo_cal import calculate_emotion_distribution

def get_monthly_summary(db: Session, member_seq: int, year: int, month: int):
    """
    월별 감정 캐릭터 요약(일별 가장 강한 감정 캐릭터)
    """
    return get_strongest_emotions_by_month(db, member_seq, year, month)

def get_daily_emotions(db: Session, member_seq: int, calendar_date):
    """
    특정 날짜의 감정 기록 전체 반환
    """
    return get_emotions_by_date(db, member_seq, calendar_date)

def update_calendar_entry(db: Session, calendar_seq: int, update_data):
    """
    감정 캘린더(및 디테일) 수정
    """
    return update_emotion_calendar(db, calendar_seq, update_data)

def create_calendar_entry(db: Session, request):
    """
    감정 캘린더 및 디테일 새로 생성
    """
    return create_emotion_calendar(db, request)

def delete_calendar_entry(db: Session, calendar_seq: int):
    """
    감정 캘린더 및 디테일 삭제
    """
    return delete_emotion_calendar(db, calendar_seq)

def create_calendar_from_text(db: Session, request):
    """
    텍스트 기반 감정 분석 후 캘린더에 저장
    """
    return save_emotion_from_text(
        db=db,
        member_seq=request.member_seq,
        calendar_date=request.calendar_date,
        text=request.text,
        title=request.title
    )

def get_monthly_emotion_distribution(db: Session, member_seq: int, year: int, month: int):
    """
    월별 감정 분포(파이차트용) 반환
    """
    from datetime import date, timedelta
    start_date = date(year, month, 1)
    end_date = (date(year + 1, 1, 1) if month == 12 else date(year, month + 1, 1)) - timedelta(days=1)
    stats = get_monthly_emotion_stats(db, member_seq, start_date, end_date)
    return calculate_emotion_distribution(stats)