from crud import get_emotion_by_seq
from sqlalchemy.orm import Session

def get_color_for_emotion(db: Session, emotion_seq: int) -> str:
    emotion = get_emotion_by_seq(db, emotion_seq)
    if not emotion:
        raise ValueError("해당 감정을 찾을 수 없습니다.")
    return emotion.color_code

# import serial
# import time

# # 블루투스 시리얼 포트 설정 (예: /dev/rfcomm0 or COM3)
# BLUETOOTH_PORT = '/dev/rfcomm0' # 아마 내(우현) 컴터로 하면 COM5일거임
# BAUD_RATE = 9600

# def send_color_to_arduino(color_code: str):
#     try:
#         with serial.Serial(BLUETOOTH_PORT, BAUD_RATE, timeout=1) as ser:
#             time.sleep(2)  # 아두이노 초기화 대기
#             # 예: "#FF0000"
#             ser.write(color_code.encode())
#     except Exception as e:
#         print(f"[ERROR] 아두이노 전송 실패: {e}")
