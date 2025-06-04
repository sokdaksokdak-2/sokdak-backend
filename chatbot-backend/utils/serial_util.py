import serial
import time

# 포트 정보 및 시리얼 설정
def send_color_to_arduino(color_code: str):
    try:
        # Windows는 'COM3' 등, macOS/Linux는 '/dev/ttyUSB0' 또는 '/dev/ttyACM0'
        ser = serial.Serial('COM5', 9600, timeout=1)
        time.sleep(2)  # 연결 안정화 대기

        # color_code를 아두이노에 전송 (예: "#FF0000\n")
        ser.write((color_code + "\n").encode())
        ser.close()
        print(f"전송 완료: {color_code}")
    except Exception as e:
        print("아두이노 연결 실패:", e)
