from sqlalchemy.orm import Session
from crud.emo_calendar import (
    get_strongest_emotions_by_month, get_emotions_by_date,
    update_emotion_calendar, create_emotion_calendar, delete_emotion_calendar,
     get_monthly_contexts
)
from crud.emo_report import get_monthly_emotion_stats
from utils.emo_cal import calculate_emotion_distribution
from schemas.emo_calendar import EmotionCalendarCreateRequest, EmotionCalendarUpdateRequest
from typing import Tuple
from models.emotion_calendar import EmotionCalendar

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

# 1. 서비스 래퍼
def update_calendar_entry(
    db: Session,
    detail_seq: int,
    member_seq: int,
    update_data: EmotionCalendarUpdateRequest,
):
    """
    감정 캘린더(및 디테일) 수정 - 래퍼
    """
    return update_emotion_calendar(db, detail_seq, member_seq, update_data)


# 2. 실제 DB 수정 함수
def update_emotion_calendar(
    db: Session,
    detail_seq: int,
    member_seq: int,
    update_data: EmotionCalendarUpdateRequest,
):
    """
    detail_seq가 로그인 사용자(member_seq)의 기록인지 확인 후
    emotion_seq / title / context 중 넘어온 값만 부분 수정
    """

def create_calendar_entry(db: Session, request):
    """
    감정 캘린더 및 디테일 새로 생성
    - create_emotion_calendar를 래핑하여 호출
    - 반환: (EmotionCalendar, EmotionCalendarDetail)
    """
    return create_emotion_calendar(db, request)

def delete_calendar_entry(db: Session, detail_seq: int, member_seq: int):
    """
    감정 캘린더 및 디테일 삭제
    """
    return delete_emotion_calendar(db, detail_seq, member_seq)


def get_monthly_emotion_distribution(db: Session, member_seq: int, year: int, month: int):
    """
    월별 감정 분포(파이차트용) 반환
    """
    from datetime import date, timedelta
    start_date = date(year, month, 1)
    end_date = (date(year + 1, 1, 1) if month == 12 else date(year, month + 1, 1)) - timedelta(days=1)
    stats = get_monthly_emotion_stats(db, member_seq, start_date, end_date)
    return calculate_emotion_distribution(stats)