import serial
import time
import logging

logger = logging.getLogger(__name__)

class ArduinoClient:
    def __init__(self, port='COM5', baudrate=9600, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None
        self._connect()

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
        if not self.ser or not self.ser.is_open:
            logger.warning("Serial port not open. Reconnecting...")
            self._connect()
            if not self.ser:
                logger.error("Cannot send color - serial connection failed.")
                return

        try:
            message = f"{color_code}\n"
            self.ser.write(message.encode())
            self.ser.flush()
            logger.info(f"Sent color code to Arduino: {color_code}")
        except Exception as e:
            logger.error(f"Failed to send color code: {e}")

