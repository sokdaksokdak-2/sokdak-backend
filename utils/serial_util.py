import serial
import time
import logging
import serial.tools.list_ports

logger = logging.getLogger(__name__)

class ArduinoClient:
    def __init__(self, port='COM4', baudrate=9600, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None
        self._connect()

    def _connect(self):
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            time.sleep(2)
            logger.info(f"[Arduino] Connected on {self.port}")
        except Exception as e:
            logger.error(f"[Arduino] Connection failed: {e}")
            self.ser = None

    def send_color(self, color_code: str):
        if self.ser and self.ser.is_open:
            try:
                self.ser.write((color_code + "\n").encode())
                logger.info(f"[Arduino] Sent: {color_code}")
            except Exception as e:
                logger.error(f"[Arduino] Send error: {e}")
