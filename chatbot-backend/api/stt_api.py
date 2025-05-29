from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from utils import get_valid_token
from services.stt_service import request_transcription, transcription_result
from db.session import get_session
from crud import summarize_and_store_stt_text, get_context_by_calendar_seq
from schemas import STTRequest, STTResponse, ContextResponse
import tempfile
import shutil
import os


# 라우터로 등록할 APIRouter 인스턴스 생성
router = APIRouter(prefix="/stt")

# 1. STT 토큰 확인
@router.get("/token")
def stt_endpoint():
    token = get_valid_token()
    # token을 이용해서 실제 STT API 호출 로직 추가 가능
    return {"token": token, "message": "토큰 발급 및 갱신 로직 작동 중"}


# 2. 음성 인식 VITO API 호출 
# return : transcribe_id ->음성 인식 결과도 요청해야 줌
@router.post("/")
async def stt(audio_file: UploadFile = File(...), language: str = "ko"):
    print("✅stt api called")
    token = get_valid_token()
    transcribe_id = request_transcription(token, audio_file)
    return {"transcribe_id": transcribe_id}


# 3. STT 처리 결과를 받아 텍스트로 반환
# return : status, text
@router.get("/{transcribe_id}")
def stt_result(transcribe_id: str):
    token = get_valid_token()
    result = transcription_result(token, transcribe_id)
    if result["status"] == "transcribing":
        return {"status": "transcribing", "message": "아직 처리중입니다. 잠시 후 다시 조회해주세요."}
    elif result["status"] == "completed":
        # 발화 텍스트들 합치기 예시
        utterances = result.get("results", {}).get("utterances", [])
        full_text = " ".join(u["msg"] for u in utterances)
        return {"status": "completed", "text": full_text}
    elif result["status"] == "failed":
        error = result.get("error", {})
        return {"status": "failed", "error": error}
    else:
        return {"status": result["status"]}
    
# 4. 텍스트 GPT API로 요약 및 DB에 저장    
@router.post("/summary", response_model=STTResponse)
def summarize_stt_text(
    request: STTRequest,
    db: Session = Depends(get_session)
):
    try:
        summary = summarize_and_store_stt_text(
            db=db,
            member_seq=request.member_seq,
            calendar_seq=request.calendar_seq,
            text=request.text
        )
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except RuntimeError as re:
        raise HTTPException(status_code=500, detail=str(re))

    return STTResponse(
        context=summary,
        calendar_seq=request.calendar_seq
    )


# 5. 저장된 context 조회 API
@router.get("/context/{calendar_seq}", response_model=ContextResponse)
def read_context_by_calendar_seq(
    calendar_seq: int,
    db: Session = Depends(get_session)
):
    context = get_context_by_calendar_seq(db, calendar_seq)
    if context is None:
        raise HTTPException(status_code=404, detail="context가 존재하지 않습니다.")
    return ContextResponse(calendar_seq=calendar_seq, context=context)

