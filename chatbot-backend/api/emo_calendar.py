from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from db.session import get_session
from crud import get_emotions_by_date, update_emotion_calendar, get_strongest_emotions_by_month, create_emotion_calendar, delete_emotion_calendar, save_emotion_from_text
from schemas import EmotionCalendarResponse, EmotionCalendarUpdateRequest, EmotionCalendarSummaryResponse, EmotionCalendarCreateRequest, EmotionCalendarFromTextRequest
from typing import List
from datetime import date

router = APIRouter()


# 1. 캘린더 월별 감정 캐릭터 데이터 가져오는 코드 (일별 가장 강한 감정 캐릭터 가져옴)
@router.get("/monthly_summary", response_model=List[EmotionCalendarSummaryResponse])
def read_monthly_emotions(
    member_seq: int = Query(...),
    year: int = Query(...),
    month: int = Query(...),
    db: Session = Depends(get_session)
):
    return get_strongest_emotions_by_month(db, member_seq, year, month)


# 2. 캘린더 상세페이지(해당 날짜 전체 게시물 불러오기)
@router.get("/daily", response_model=List[EmotionCalendarResponse])
def read_emo_calendar(
    member_seq: int = Query(...),
    calendar_date: date = Query(...),
    db: Session = Depends(get_session)
):
    return get_emotions_by_date(db, member_seq, calendar_date)


# 3. 캘린더 내용 수정 (감정 캐릭터, 제목, 메모 등 변경)
@router.put("/{calendar_seq}")
def update_emo_calendar(
    calendar_seq: int,
    update_data: EmotionCalendarUpdateRequest,
    db: Session = Depends(get_session)
):
    updated = update_emotion_calendar(db, calendar_seq, update_data)
    
    if updated is None:
        raise HTTPException(status_code=404, detail="EmotionCalendar not found")

    return {"message": "Update successful", "calendar_seq": calendar_seq}


# 4. 캘린더에 새로운 내용 입력 (사용자가 감정, 메모, 제목 직접 입력)
@router.post("/")
def create_calendar_entry(
    request: EmotionCalendarCreateRequest,
    db: Session = Depends(get_session)
):
    result = create_emotion_calendar(db, request)
    return {
        "calendar_seq": result.calendar_seq,
        "message": "감정 기록이 추가되었습니다."
    }


# 5. 캘린더 내용 삭제  (calendar_seq 기준)
@router.delete("/{calendar_seq}")
def delete_calendar_entry(
    calendar_seq: int,
    db: Session = Depends(get_session)
):
    success = delete_emotion_calendar(db, calendar_seq)

    if not success:
        raise HTTPException(status_code=404, detail="해당 게시글을 찾을 수 없습니다.")

    return {"message": "게시글이 성공적으로 삭제되었습니다."}

@router.post("/from-text", response_model=EmotionCalendarResponse)
def create_calendar_from_text(
    request: EmotionCalendarFromTextRequest,
    db: Session = Depends(get_session)
):
    return save_emotion_from_text(
        db=db,
        member_seq=request.member_seq,
        calendar_date=request.calendar_date,
        text=request.text,
        title=request.title
    )
