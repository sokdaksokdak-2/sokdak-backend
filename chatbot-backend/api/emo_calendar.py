from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from db.session import get_session
from schemas.emo_calendar import (
    EmotionCalendarResponse, EmotionCalendarUpdateRequest,
    EmotionCalendarSummaryResponse, EmotionCalendarCreateRequest,
    EmotionCalendarFromTextRequest
)
from typing import List
from datetime import date
from services.emo_calendar_service import (
    get_monthly_summary, get_daily_emotions, update_calendar_entry,
    create_calendar_entry, delete_calendar_entry, create_calendar_from_text
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
@router.put("/{calendar_seq}")
def update_emo_calendar(
    calendar_seq: int,
    update_data: EmotionCalendarUpdateRequest,
    db: Session = Depends(get_session)
):
    """
    감정 기록 수정 API
    - calendar_seq: 수정할 감정 캘린더 항목의 시퀀스
    - update_data: 제목, 메모, 감정 캐릭터 등의 수정 내용
    - 반환: 성공 메시지 또는 404 에러
    """
    updated = update_calendar_entry(db, calendar_seq, update_data)
    if updated is None:
        raise HTTPException(status_code=404, detail="EmotionCalendar not found")
    return {"message": "Update successful", "calendar_seq": calendar_seq}


# 4. 캘린더에 새로운 내용 입력 (사용자가 감정, 메모, 제목 직접 입력)
@router.post("/")
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
        "message": "감정 기록이 추가되었습니다."
    }


# 5. 캘린더 내용 삭제  (calendar_seq 기준)
@router.delete("/{calendar_seq}")
def delete_calendar_entry_api(
    calendar_seq: int,
    db: Session = Depends(get_session)
):
    """
    감정 기록 삭제 API
    - calendar_seq: 삭제할 감정 캘린더 항목의 시퀀스
    - 반환: 성공 메시지 또는 404 에러
    """
    success = delete_calendar_entry(db, calendar_seq)
    if not success:
        raise HTTPException(status_code=404, detail="해당 게시글을 찾을 수 없습니다.")
    return {"message": "게시글이 성공적으로 삭제되었습니다."}



@router.post("/from-text", response_model=EmotionCalendarResponse)
def create_calendar_from_text_api(
    request: EmotionCalendarFromTextRequest,
    db: Session = Depends(get_session)
):
    """
    텍스트 기반 감정 분석 후 감정 기록 생성 API
    - request: raw_text, calendar_date, member_seq
    - 내부에서 GPT API를 활용해 감정 분석 및 기록 생성
    - 반환: 생성된 EmotionCalendar 데이터
    """
    return create_calendar_from_text(db, request)
