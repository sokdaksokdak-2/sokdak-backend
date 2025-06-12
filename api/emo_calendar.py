from fastapi import APIRouter, Depends, Query, HTTPException, Body
from sqlalchemy.orm import Session
from db.session import get_session
from schemas import (
    EmotionCalendarResponse, EmotionCalendarUpdateRequest,
    EmotionCalendarSummaryResponse, EmotionCalendarCreateRequest,
    EmotionCalendarFromTextRequest, CalendarCreateResponse
)
from typing import List
from datetime import date
from services.emo_calendar_service import (
    get_monthly_summary, get_daily_emotions, update_calendar_entry,
    create_calendar_entry, delete_calendar_entry
)

router = APIRouter()


# 1. 캘린더 월별 감정 캐릭터 데이터 가져오는 코드 (일별 가장 강한 감정 캐릭터 가져옴)
@router.get("/monthly_summary", response_model=List[EmotionCalendarSummaryResponse])
def read_monthly_emotions(
    member_seq: int = Query(...),
    year: int = Query(...),
    month: int = Query(...),
    db: Session = Depends(get_session)
):
    """
    월별 감정 요약 조회 API
    - member_seq: 회원 시퀀스
    - year, month: 조회할 연/월
    - 반환: 일별로 가장 강한 감정을 가진 EmotionCalendarSummary 리스트
    """
    return get_monthly_summary(db, member_seq, year, month)


# 2. 캘린더 상세페이지(해당 날짜 전체 게시물 불러오기)
@router.get("/daily", response_model=List[EmotionCalendarResponse])
def read_emo_calendar(
    member_seq: int = Query(...),
    calendar_date: date = Query(...),
    db: Session = Depends(get_session)
):
    """
    특정 날짜의 감정 기록 전체 조회 API
    - member_seq: 회원 시퀀스
    - calendar_date: 조회할 날짜 (예시: 2025-05-31)
    - 반환: 해당 날짜의 EmotionCalendar 리스트
    """
    return get_daily_emotions(db, member_seq, calendar_date)


# 3. 캘린더 내용 수정 (감정 캐릭터, 제목, 메모 등 변경)
@router.put("/{detail_seq}")
def update_calendar_entry_api(
    detail_seq: int,
    update_data: EmotionCalendarUpdateRequest,
    member_seq: int = Query(...),           # 또는 Depends(get_current_user)
    db: Session = Depends(get_session),
):
    ok = update_calendar_entry(db, detail_seq, member_seq, update_data)
    if not ok:
        raise HTTPException(
            status_code=404,
            detail="수정 권한이 없거나 존재하지 않는 감정 기록입니다.",
        )
    return {"message": "감정 기록이 성공적으로 수정되었습니다."}




# 4. 캘린더에 새로운 내용 입력 (사용자가 감정, 메모, 제목 직접 입력
@router.post("/", response_model=CalendarCreateResponse)

def create_calendar_entry_api(
    request: EmotionCalendarCreateRequest,
    db: Session = Depends(get_session)
):
    """
    감정 기록 직접 작성 API
    - request: 감정, 제목, 메모, 날짜 등의 데이터
    - 반환: 생성된 calendar_seq 및 성공 메시지
    """
    result = create_calendar_entry(db, request)
    return {
        "calendar_seq": result.calendar_seq,
        "calendar_date": result.calendar_date,
        "member_seq": result.member_seq,
        "title": request.title,
        "context": request.context,
        "emotion_seq": request.emotion_seq


    }


# 5. 캘린더 내용 삭제  (calendar_seq 기준)
@router.delete("/{calendar_seq}")
def delete_calendar_entry_api(
    detail_seq: int,
    member_seq: int,
    db: Session = Depends(get_session)
):
    """
    감정 기록 삭제 API
    - detail_seq: 삭제할 감정 캘린더 항목의 시퀀스
    - 반환: 성공 메시지 또는 404 에러
    """
    success = delete_calendar_entry(db, detail_seq, member_seq)
    if not success:
        raise HTTPException(status_code=404, detail="해당 게시글을 찾을 수 없습니다.")
    return {"message": "게시글이 성공적으로 삭제되었습니다."}


