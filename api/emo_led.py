from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas import EmotionRequest, EmotionResponse
from services import get_color_for_emotion
from utils import ArduinoClient
from utils import send_color_to_arduino

from db import get_session  # DB 세션 종속성

router = APIRouter()

@router.post("/emotion/color", response_model=EmotionResponse)
def apply_emotion_color(req: EmotionRequest, db: Session = Depends(get_session)):
    color = get_color_for_emotion(db, req.emotion_seq)

    arduino_client = ArduinoClient()
    arduino_client.send_color(color)
    send_color_to_arduino(color)
    return EmotionResponse(color_code=color)

@router.post("/test/send-color")
def test_send_color(color_code: str):
    """
    임의의 HEX 색상 코드를 아두이노로 전송합니다.
    예: "#FF0000" (빨강), "#00FF00" (초록)
    """
    if not (color_code.startswith("#") and len(color_code) == 7):
        return {"error": "색상 코드는 '#RRGGBB' 형식이어야 합니다."}

    arduino_client = ArduinoClient()
    arduino_client.send_color(color_code)

    return {"message": f"{color_code} 전송 완료"}

