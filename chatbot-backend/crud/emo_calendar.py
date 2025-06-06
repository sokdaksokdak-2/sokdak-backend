from sqlalchemy.orm import Session
from models import EmotionCalendar, EmotionCalendarDetail, Emotion, SourceType
from schemas.emo_calendar import EmotionCalendarResponse, EmotionCalendarUpdateRequest, EmotionCalendarSummaryResponse, EmotionCalendarCreateRequest
from sqlalchemy import func, extract
from datetime import date, timedelta, datetime, UTC
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, Query
import os
from openai import OpenAI
import openai

from utils import OPENAI_API_KEY





# 1. 캘린더 월별 감정 캐릭터 데이터 가져오는 코드 (하루 중 감정의 강도가 제일 높은 캐릭터 가져옴)
# 회색 물음표 캐릭터 이미지 URL
default_gray_image_url = os.getenv("https://your-cdn.com/images/question_gray.png") # 감정 캐릭터 이미지가 아닌 회색 사람 이미지 url

def get_strongest_emotions_by_month(db: Session, member_seq: int, year: int, month: int):
    """
    월별 각 날짜별로 가장 강한 감정 캐릭터 이미지 URL을 반환
    """
       
    # 1-1. 날짜 범위 생성
    first_day = date(year, month, 1)
    last_day = (date(year + 1, 1, 1) if month == 12 else date(year, month + 1, 1)) - timedelta(days=1)

    all_dates = [first_day + timedelta(days=i) for i in range((last_day - first_day).days + 1)]

    # 1-2. 서브쿼리: 감정 점수(emotion_score)와 감정 번호(emotion_seq)를 날짜별로 정리
    subquery = (
        db.query(
            EmotionCalendar.calendar_date.label("calendar_date"),
            Emotion.character_image_url.label("character_image_url"),
            Emotion.emotion_intensity.label("emotion_intensity"),
            Emotion.emotion_seq.label("emotion_seq")
        )
        .join(EmotionCalendarDetail, EmotionCalendar.calendar_seq == EmotionCalendarDetail.calendar_seq)
        .join(Emotion, EmotionCalendarDetail.emotion_seq == Emotion.emotion_seq)
        .filter(
            EmotionCalendar.member_seq == member_seq,
            extract("year", EmotionCalendar.calendar_date) == year,
            extract("month", EmotionCalendar.calendar_date) == month
        )
        .subquery()
    )

    # 1-3. 날짜별로 가장 높은 emotion_intensity, 그 중 가장 낮은 emotion_seq 선택
    best_emotion_subquery = (
        db.query(
            subquery.c.calendar_date,
            func.max(subquery.c.emotion_intensity).label("max_intensity")
        )
        .group_by(subquery.c.calendar_date)
        .subquery()
    )

    final_query = (
        db.query(subquery.c.calendar_date, subquery.c.character_image_url)
        .join(
            best_emotion_subquery,
            (subquery.c.calendar_date == best_emotion_subquery.c.calendar_date) &
            (subquery.c.emotion_intensity == best_emotion_subquery.c.max_intensity)
        )
        .order_by(subquery.c.calendar_date, subquery.c.emotion_seq)  # 낮은 emotion_seq 우선
    )

    results = final_query.distinct(subquery.c.calendar_date).all()

    # 1-4. 날짜별 결과 정리
    date_to_image = {r.calendar_date: r.character_image_url for r in results}

    response = [
        EmotionCalendarSummaryResponse(
            calendar_date=d,
            character_image_url=date_to_image.get(d, default_gray_image_url)
        )
        for d in all_dates
    ]

    return response


# 2. 캘린더 상세페이지(해당 날짜 전체 게시물등 불러오기)
def get_emotions_by_date(db: Session, member_seq: int, calendar_date: str):
    """
    특정 날짜의 감정 기록 전체 반환
    """

    result = (
        db.query(Emotion.character_image_url,
                 EmotionCalendarDetail.context,
                 EmotionCalendar.calendar_date)
        .join(EmotionCalendarDetail, EmotionCalendar.calendar_seq == EmotionCalendarDetail.calendar_seq)
        .join(Emotion, EmotionCalendarDetail.emotion_seq == Emotion.emotion_seq)
        .filter(EmotionCalendar.member_seq == member_seq,
                EmotionCalendar.calendar_date == calendar_date)
        .all()
    )

    return [EmotionCalendarResponse(
        character_image_url=row[0],
        context=row[1],
        calendar_date=row[2]
    ) for row in result]


# 3. 캘린더 내용 수정 (감정 캐릭터, 제목, context 등 변경)
def update_emotion_calendar(db: Session, calendar_seq: int, update_data: EmotionCalendarUpdateRequest):
    """
    감정 캘린더(및 디테일) 수정
    """

    # 3-1. 기본 감정 캘린더 조회
    calendar = db.query(EmotionCalendar).filter(EmotionCalendar.calendar_seq == calendar_seq).first()
    if not calendar:
        return None

    # 3-2. 제목과 메모는 EmotionCalendar에서 직접 수정
    if update_data.title is not None:
        calendar.title = update_data.title   # 제목은 추 후에 DB에 추가하게 되면 주석 푸는거로
    if update_data.context is not None:
        calendar.context = update_data.context

    # 3-3. 감정 캐릭터 이미지 → Emotion 연결 관계 수정
    if update_data.emotion_seq is not None:
        detail = db.query(EmotionCalendarDetail).filter(
            EmotionCalendarDetail.calendar_seq == calendar_seq
        ).first()

        if detail:
            detail.emotion_seq = update_data.emotion_seq
            # detail.emotion_score = ...  # 제거
        else:
            new_detail = EmotionCalendarDetail(
                calendar_seq=calendar_seq,
                emotion_seq=update_data.emotion_seq
                # emotion_score=...  # 제거
            )
            db.add(new_detail)

    db.commit()
    db.refresh(calendar)
    return calendar


# 4. 캘린더에 새로운 내용 입력 (사용자가 감정, 메모, 제목 직접 입력)
def create_emotion_calendar(db: Session, request: EmotionCalendarCreateRequest):
    """
    감정 캘린더 및 디테일 새로 생성
    """
    # 1. EmotionCalendar 테이블에 새 레코드 추가
    new_calendar = EmotionCalendar(
        member_seq=request.member_seq,
        calendar_date=request.calendar_date,
        context=request.context,
        character_image_url=None  # 캐릭터 이미지는 Emotion을 통해 가져오기 때문에 저장 안 함
    )
    db.add(new_calendar)
    db.flush()  # calendar_seq 확보

    # 2. EmotionCalendarDetail 테이블에 감정 정보 추가
    new_detail = EmotionCalendarDetail(
        calendar_seq=new_calendar.calendar_seq,
        emotion_seq=request.emotion_seq,
        title=request.title,
        source=SourceType.USER,         # ✅ 직접 작성이므로 고정
        emotion_score=1,
        context=request.context
    )
    db.add(new_detail)

    # 3. 커밋 및 결과 반환
    db.commit()
    db.refresh(new_calendar)
    return new_calendar

# 5. 캘린더 내용 삭제 (calendar_seq 기준)
def delete_emotion_calendar(db: Session, calendar_seq: int) -> bool:
    """
    감정 캘린더 및 디테일 삭제
    """
    # 관련된 EmotionCalendarDetail 먼저 삭제
    db.query(EmotionCalendarDetail).filter(
        EmotionCalendarDetail.calendar_seq == calendar_seq
    ).delete()

    # EmotionCalendar 삭제
    deleted = db.query(EmotionCalendar).filter(
        EmotionCalendar.calendar_seq == calendar_seq
    ).delete()

    db.commit()
    return deleted > 0


def get_monthly_emotion_stats(db: Session, member_seq: int, start_date: date, end_date: date):
    """
    월별 감정별 (name_kr, intensity, count) raw 데이터 반환
    """
    return db.query(
        Emotion.name_kr,
        Emotion.emotion_intensity,
        func.count().label("count")
    ).join(EmotionCalendarDetail, EmotionCalendar.calendar_seq == EmotionCalendarDetail.calendar_seq
    ).join(Emotion, EmotionCalendarDetail.emotion_seq == Emotion.emotion_seq
    ).filter(
        EmotionCalendar.member_seq == member_seq,
        EmotionCalendar.calendar_date >= start_date,
        EmotionCalendar.calendar_date <= end_date
    ).group_by(Emotion.name_kr, Emotion.emotion_intensity).all()

def get_monthly_contexts(db: Session, member_seq: int, start_date: date, end_date: date):
    """
    월별 감정 메모 context 리스트 반환
    """
    contexts = db.query(EmotionCalendarDetail.context
    ).join(EmotionCalendar, EmotionCalendar.calendar_seq == EmotionCalendarDetail.calendar_seq
    ).filter(
        EmotionCalendar.member_seq == member_seq,
        EmotionCalendar.calendar_date >= start_date,
        EmotionCalendar.calendar_date <= end_date,
        EmotionCalendarDetail.context.isnot(None)
    ).all()
    return [c[0] for c in contexts if c[0]]


# 6. STT 텍스트 기반 감정 분석 및 저장
def save_emotion_from_text(db: Session, member_seq: int, calendar_date: date, text: str, title: str = None):
    """
    텍스트 기반 감정 분석 후 캘린더에 저장
    """
    from services import analyze_emotion_from_text
    emotion_data = analyze_emotion_from_text(text)
    emotion = db.query(Emotion).filter(
        Emotion.name_en == emotion_data["emotion_name_en"],
        Emotion.emotion_intensity == emotion_data["emotion_intensity"]
    ).first()
    if not emotion:
        raise ValueError("해당 감정 정보가 Emotion 테이블에 없습니다.")

    new_calendar = EmotionCalendar(
        member_seq=member_seq,
        calendar_date=calendar_date
    )
    db.add(new_calendar)
    db.flush()

    new_detail = EmotionCalendarDetail(
        calendar_seq=new_calendar.calendar_seq,
        emotion_seq=emotion.emotion_seq,
        title=title,
        context=text,
        source="ai"
    )
    db.add(new_detail)
    db.commit()
    return new_calendar

def save_emotion_calendar(db: Session, member_seq: int, calendar_date: date, emotion_seq: int, context: str, title: str | None = None):
    new_calendar = EmotionCalendar(
        member_seq=member_seq,
        calendar_date=calendar_date
    )
    db.add(new_calendar)
    db.flush()  # calendar_seq 확보

    new_detail = EmotionCalendarDetail(
        calendar_seq=new_calendar.calendar_seq,
        emotion_seq=emotion_seq,
        context=context,
        title=title,
        source="ai"
    )
    db.add(new_detail)
    db.commit()

    return new_calendar

    