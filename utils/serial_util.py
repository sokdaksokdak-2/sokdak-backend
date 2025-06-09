import serial
import time

class ArduinoClient:
    def __init__(self, port='COM4', baudrate=9600, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None
        self._connect()

    def _auto_detect_port(self):
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            if "Arduino" in p.description or "USB-SERIAL" in p.description:
                logger.info(f"[Arduino] Detected port: {p.device}")
                return p.device
        logger.warning("[Arduino] No Arduino device detected.")
        return "COM4"  # fallback (필요 시 None 반환하고 예외 처리도 가능)

    def _connect(self):
        try:
            if self.ser and self.ser.is_open:
                logger.info("Serial port already open.")
                return
            self.ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            time.sleep(2)
            logger.info(f"Arduino connected on {self.port} at {self.baudrate} baud.")
        except (serial.SerialException, PermissionError) as e:
            logger.error(f"Failed to connect to Arduino on {self.port}: {e}")
            self.ser = None
            
    def send_color(self, color_code: str):
        if self.ser.is_open:
            self.ser.write(color_code.encode())  # 예: "#FF0000"


    # 포트 정보 및 시리얼 설정
    def send_color_to_arduino(color_code: str):
        try:
            # Windows는 'COM3' 등, macOS/Linux는 '/dev/ttyUSB0' 또는 '/dev/ttyACM0'
            ser = serial.Serial('COM4', 9600, timeout=1)
            time.sleep(2)  # 연결 안정화 대기

            # color_code를 아두이노에 전송 (예: "#FF0000\n")
            ser.write((color_code + "\n").encode())
            ser.close()
            print(f"전송 완료: {color_code}")
        except Exception as e:
            print("아두이노 연결 실패:", e)

