import requests
import json
from fastapi import UploadFile, HTTPException

VITO_TRANSCRIBE_URL = "https://openapi.vito.ai/v1/transcribe"

def request_transcription(token: str, audio_file: UploadFile) -> str:
    headers = {"Authorization": f"Bearer {token}"}
    config = {"model_name": "whisper", "language": "ko"}

    files = {
        "file": (audio_file.filename, audio_file.file, audio_file.content_type)
    }
    data = {"config": json.dumps(config)}

    response = requests.post(VITO_TRANSCRIBE_URL, headers=headers, files=files, data=data)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=f"STT 요청 실패: {response.text}")

    return response.json()["id"]

def transcription_result(token: str, transcribe_id: str) -> dict:
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{VITO_TRANSCRIBE_URL}/{transcribe_id}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=f"STT 결과 조회 실패: {response.text}")
    return response.json()

def parse_transcription_result(result: dict) -> dict:
    status = result.get("status")
    
    if status == "transcribing":
        return {"status": "transcribing", "message": "아직 처리중입니다. 잠시 후 다시 조회해주세요."}
    
    if status == "completed":
        utterances = result.get("results", {}).get("utterances", [])
        full_text = " ".join(u["msg"] for u in utterances)
        return {"status": "completed", "text": full_text}
    
    if status == "failed":
        return {"status": "failed", "error": result.get("error", {})}
    
    return {"status": status}
