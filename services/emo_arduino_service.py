from crud import get_emotion_by_seq
from utils import ArduinoClient
from sqlalchemy.orm import Session
from utils import redis_client
import logging
import json
import logging

logger = logging.getLogger(__name__)

class ArduinoService:
    def __init__(self, db: Session):
        self.db = db
        self.arduino = ArduinoClient()

    async def detect_and_send_emotion_change(self, member_seq: int, current_emotion_seq: int):
        redis_key = f"chat_history:{member_seq}"
        history = await redis_client.lrange(redis_key, 0, 1)

        if len(history) < 2:
            logger.info("[Arduino] 이전 대화 없음 (비교 불가)")
            return

        try:
            previous_raw = history[1]  # 두 번째 최신 기록
            previous = json.loads(previous_raw)

            # 여기서 안전하게 추출
            prev_emotion_seq = previous.get("chatbot_response", {}).get("emotion_seq")

            if prev_emotion_seq is None:
                raise ValueError("emotion_seq is None in previous Redis data")

            prev_emotion_seq = int(prev_emotion_seq)

        except (ValueError, TypeError, KeyError, json.JSONDecodeError) as e:
            logger.warning(f"[Arduino] Redis 감정 파싱 실패: {e} | 데이터: {history[1]}")
            return

        if prev_emotion_seq != current_emotion_seq:
            emotion = get_emotion_by_seq(self.db, current_emotion_seq)
            if emotion:
                self.arduino.send_color(emotion.color_code)
            else:
                logger.warning(f"[Arduino] DB에서 감정 정보를 찾지 못함: {current_emotion_seq}")
        else:
            logger.info("[Arduino] 감정 변화 없음 (색상 전송 안 함)")


