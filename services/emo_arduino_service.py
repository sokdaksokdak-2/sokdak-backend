from crud import get_emotion_by_seq
from utils import ArduinoClient
from sqlalchemy.orm import Session
from utils import redis_client

import json


class ArduinoService:
    def __init__(self, db: Session):
        self.db = db
        self.arduino = ArduinoClient()

    async def detect_and_send_emotion_change(self, member_seq: int, current_emotion_seq: int):

        # Redis에서 최근 대화 가져오기
        redis_key = f"chat_history:{member_seq}"
        history = await redis_client.lrange(redis_key, -2, -1)  # 마지막 2개 대화

        if len(history) < 2:
            return  # 이전 감정이 없음 → 비교 불가

        # 마지막 대화의 감정
        previous = json.loads(history[-2])
        prev_emotion_seq = int(previous["emotion_seq"])

        if prev_emotion_seq != current_emotion_seq:
            # 감정 변화 감지
            emotion = get_emotion_by_seq(self.db, current_emotion_seq)
            if emotion:
                self.arduino.send_color(emotion.color_code)
