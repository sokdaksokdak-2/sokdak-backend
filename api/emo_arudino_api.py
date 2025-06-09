from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_session
from schemas import EmotionChangeRequest
from services import ArduinoService

router = APIRouter()


@router.post("/send-color-if-changed")
async def send_emotion_color_if_changed(
    request: EmotionChangeRequest,
    db: Session = Depends(get_session)
):
    service = ArduinoService(db)
    await service.detect_and_send_emotion_change(
        member_seq=request.member_seq,
        current_emotion_seq=request.current_emotion_seq
    )
    return {"status": "checked"}
