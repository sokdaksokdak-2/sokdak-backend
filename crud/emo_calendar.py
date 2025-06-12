from sqlalchemy.orm import Session
from models import EmotionCalendar, EmotionCalendarDetail, Emotion, SourceType, EmotionDetail
from schemas.emo_calendar import EmotionCalendarResponse, EmotionCalendarUpdateRequest, EmotionCalendarSummaryResponse, EmotionCalendarCreateRequest
from sqlalchemy import func, extract
from datetime import date, timedelta, datetime, UTC
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, Query
from openai import OpenAI
import os

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
            EmotionDetail.emotion_score.label("emotion_score"),
            Emotion.emotion_seq.label("emotion_seq")
        )
        .join(EmotionCalendarDetail, EmotionCalendar.calendar_seq == EmotionCalendarDetail.calendar_seq)
        .join(Emotion, EmotionCalendarDetail.emotion_seq == Emotion.emotion_seq)
        .join(EmotionDetail, Emotion.emotion_seq == EmotionDetail.emotion_seq) 
        .filter(
            EmotionCalendar.member_seq == member_seq,
            extract("year", EmotionCalendar.calendar_date) == year,
            extract("month", EmotionCalendar.calendar_date) == month
        )
        .subquery()
    )

    # 1-3. 날짜별로 가장 높은 emotion_score, 그 중 가장 낮은 emotion_seq 선택
    best_emotion_subquery = (
        db.query(
            subquery.c.calendar_date,
            func.max(subquery.c.emotion_score).label("max_score")
        )
        .group_by(subquery.c.calendar_date)
        .subquery()
    )

    final_query = (
        db.query(subquery.c.calendar_date, subquery.c.emotion_seq)
        .join(
            best_emotion_subquery,
            (subquery.c.calendar_date == best_emotion_subquery.c.calendar_date) &
            (subquery.c.emotion_score == best_emotion_subquery.c.max_score)
        )
        .order_by(subquery.c.calendar_date, subquery.c.emotion_seq)  # 낮은 emotion_seq 우선
    )

    results = final_query.distinct(subquery.c.calendar_date).all()

    # 1-4. 날짜별 결과 정리
    date_to_image = {r.calendar_date: r.emotion_seq for r in results}

    response = [
        EmotionCalendarSummaryResponse(
            calendar_date=d,
            emotion_seq=date_to_image.get(d, default_gray_image_url)
        )
        for d in all_dates
    ]

    return response


# 2. 캘린더 상세페이지(해당 날짜 전체 게시물등 불러오기)
def get_emotions_by_date(
    db: Session,
    member_seq: int,
    calendar_date: date,       # ← 타입을 date 로
):
    """
    특정 날짜의 감정 기록 전체 반환
    """

    rows = (
        db.query(
            EmotionCalendarDetail.detail_seq,
            EmotionCalendarDetail.emotion_seq,
            EmotionCalendarDetail.title,
            EmotionCalendarDetail.context,
            EmotionCalendar.calendar_date,
        )
        .join(                       # ① 부모(EmotionCalendar)와 조인
            EmotionCalendar,
            EmotionCalendar.calendar_seq == EmotionCalendarDetail.calendar_seq,
        )
        .filter(
            EmotionCalendar.member_seq == member_seq,
            EmotionCalendar.calendar_date == calendar_date,
        )
        .all()
    )

    return [
        EmotionCalendarResponse(
            detail_seq=row[0],
            emotion_seq=row[1],
            title=row[2],
            context=row[3],
            calendar_date=row[4],
        )
        for row in rows
    ]


# 3. 캘린더 내용 수정 (감정 캐릭터, 제목, context 등 변경)
def update_emotion_calendar(
    db: Session,
    detail_seq: int,
    member_seq: int,
    update_data: EmotionCalendarUpdateRequest,
):
    """
    감정 캘린더 디테일 수정 (소유권 검증 포함)
    반환: True = 수정 성공 / False = 권한 없음·미존재
    """
    # 1️⃣ detail_seq 가 member_seq 소유인지 확인
    detail = (
        db.query(EmotionCalendarDetail)
        .join(
            EmotionCalendar,
            EmotionCalendar.calendar_seq == EmotionCalendarDetail.calendar_seq,
        )
        .filter(
            EmotionCalendarDetail.detail_seq == detail_seq,
            EmotionCalendar.member_seq == member_seq,
        )
        .first()
    )
    if detail is None:
        return False     # 404 사유: 없음 또는 내 소유 아님

    # 2️⃣ 부분 업데이트
    if update_data.emotion_seq is not None:
        detail.emotion_seq = update_data.emotion_seq
    if update_data.title is not None:
        detail.title = update_data.title
    if update_data.context is not None:
        detail.context = update_data.context

    # 3️⃣ 커밋 & 완료
    db.commit()
    return True




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
        emotion_seq=request.emotion_seq  # 캐릭터 이미지는 Emotion을 통해 가져오기 때문에 저장 안 함
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
def delete_emotion_calendar(db: Session, detail_seq: int, member_seq: int) -> bool:
    """
    해당 사용자의 감정 캘린더 상세(detail) 삭제
    """
    # 1. detail_seq에 해당하는 상세 정보를 가져오면서, 그 부모 캘린더의 member_seq도 검증
    detail = (
        db.query(EmotionCalendarDetail)
        .join(EmotionCalendar, EmotionCalendarDetail.calendar_seq == EmotionCalendar.calendar_seq)
        .filter(
            EmotionCalendarDetail.detail_seq == detail_seq,
            EmotionCalendar.member_seq == member_seq  # 사용자 소유 여부 확인
        )
        .first()
    )

    if not detail:
        return False  # detail_seq가 없거나, 다른 사람의 캘린더

    # 2. 삭제 수행
    db.delete(detail)
    db.commit()
    return True



def get_monthly_emotion_stats(db: Session, member_seq: int, start_date: date, end_date: date):
    """
    월별 감정별 (name_kr, emotion_score, count) raw 데이터 반환
    """
    return db.query(
        Emotion.name_kr,
        EmotionDetail.emotion_score,
        func.count().label("count")
    ).join(EmotionCalendarDetail, EmotionCalendar.calendar_seq == EmotionCalendarDetail.calendar_seq
    ).join(Emotion, EmotionCalendarDetail.emotion_seq == Emotion.emotion_seq
    ).join(EmotionDetail, Emotion.emotion_seq == EmotionDetail.emotion_seq
    ).filter(
        EmotionCalendar.member_seq == member_seq,
        EmotionCalendar.calendar_date >= start_date,
        EmotionCalendar.calendar_date <= end_date
    ).group_by(Emotion.name_kr, EmotionDetail.emotion_score).all()

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


def save_emotion_calendar(db: Session, member_seq: int, emotion_seq: int, emotion_score: int, title: str, context: str, source: str):
    ''' 챗봇 대화 내용 저장 요약
    '''
    new_calendar = EmotionCalendar(
        member_seq=member_seq,
        calendar_date=datetime.now(UTC).date(),        
    )
    db.add(new_calendar)
    db.commit()

    new_calendar_detail = EmotionCalendarDetail(
        calendar_seq=new_calendar.calendar_seq,
        member_seq=member_seq,
        emotion_seq=emotion_seq,
        emotion_score=emotion_score,
        title=title,
        context=context,
        created_at=datetime.now(UTC),
        source=source
    )

    db.add(new_calendar)
    db.add(new_calendar_detail)
    db.commit()

    return new_calendar_detail
    