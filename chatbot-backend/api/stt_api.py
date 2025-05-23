from fastapi import APIRouter, UploadFile, File, HTTPException
from utils.vito_token_manager import get_valid_token
from services.stt_service import request_transcription, transcription_result
import tempfile
import shutil
import os

# 라우터로 등록할 APIRouter 인스턴스 생성
router = APIRouter()

@router.get("/stt-token")
def stt_endpoint():
    token = get_valid_token()
    # token을 이용해서 실제 STT API 호출 로직 추가 가능
    return {"token": token, "message": "토큰 발급 및 갱신 로직 작동 중"}


# 음성 인식 VITO API 호출 
# return : transcribe_id ->음성 인식 결과도 요청해야 줌
@router.post("/stt")
async def stt(audio_file: UploadFile = File(...), language: str = "ko"):
    print("✅stt api called")
    token = get_valid_token()
    transcribe_id = request_transcription(token, audio_file)
    return {"transcribe_id": transcribe_id}

# 음성 인식 결과 조회
# return : status, text
@router.get("/stt/{transcribe_id}")
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


