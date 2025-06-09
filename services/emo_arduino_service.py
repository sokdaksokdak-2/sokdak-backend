from crud import get_emotion_by_seq
from utils import ArduinoClient
from sqlalchemy.orm import Session
from utils import redis_client

import json

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class ArduinoService:
    def __init__(self, db: Session):
        self.db = db
        self.arduino = ArduinoClient()

    async def detect_and_send_emotion_change(self, member_seq: int, current_emotion_seq: int):
        redis_key = f"chat_history:{member_seq}"
        # 최신 2개 기록 가져오기 (0부터 1까지)
        history =  await redis_client.lrange(redis_key, 0, 1)

        if len(history) < 2:
            logger.info("[Arduino] 이전 대화 없음 (비교 불가)")
            return

        try:
            previous = json.loads(history[1])  # 두 번째 최신 기록 (이전 기록)
            prev_emotion_seq_raw = previous.get("chatbot_response", {}).get("emotion_seq")

            if prev_emotion_seq_raw is None:
                raise ValueError("emotion_seq is None in previous Redis data")

            prev_emotion_seq = int(prev_emotion_seq_raw)
            
        except (ValueError, TypeError, KeyError) as e:
            logger.warning(f"[Arduino] Redis 감정 파싱 실패: {e} | 데이터: {previous}")
            return

        logger.info(f"[Arduino] 감정 비교: 이전={prev_emotion_seq}, 현재={current_emotion_seq}")

        if prev_emotion_seq != current_emotion_seq:
            emotion =  get_emotion_by_seq(self.db, current_emotion_seq)
            if emotion:
                logger.info(f"[Arduino] 감정 변화 감지, 색상 전송: {emotion.color_code}")
                self.arduino.send_color(emotion.color_code)
            else:
                logger.warning(f"[Arduino] DB에서 감정 정보를 찾지 못함: {current_emotion_seq}")
        else:
            logger.info("[Arduino] 감정 변화 없음 (색상 전송 안 함)")

