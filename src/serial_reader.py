import serial
import time
from config import SERIAL_PORT, BAUD_RATE


class RFIDSerial:
    def __init__(self):
        self.ser = serial.Serial(
            SERIAL_PORT,
            BAUD_RATE,
            timeout=2
        )

        time.sleep(2)
        self.ser.reset_input_buffer()

        print(f"[Serial] Connected on {SERIAL_PORT}")

    def read_rfid(self):
        try:
            line = self.ser.readline().decode(
                errors="ignore"
            ).strip()

            if not line:
                return None, None

            print(f"[Serial] RX: {line}")

            if "," not in line:
                return None, None

            name, srn = line.split(",", 1)

            return name.strip(), srn.strip()

        except Exception as e:
            print(f"[Serial] Read error: {e}")
            return None, None

    def send_result(self, status):
        try:
            self.ser.write((status + "\n").encode())
            self.ser.flush()

            print(f"[Serial] TX: {status}")

        except Exception as e:
            print(f"[Serial] Send error: {e}")

    def close(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("[Serial] Closed")