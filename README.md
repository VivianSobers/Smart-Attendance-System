# Smart Attendance System — RFID + Face Recognition

![IoT](https://img.shields.io/badge/IoT-RFID%20%2B%20Sensors-FF6F00?style=for-the-badge)
![Language](https://img.shields.io/badge/Python-Automation-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Embedded](https://img.shields.io/badge/Arduino-Hardware%20Layer-00979D?style=for-the-badge&logo=arduino&logoColor=white)
![Computer Vision](https://img.shields.io/badge/OpenCV-Face%20Detection-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![AI](https://img.shields.io/badge/DeepFace-Facial%20Recognition-8E44AD?style=for-the-badge)
![Database](https://img.shields.io/badge/SQLite-Local%20Storage-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Security](https://img.shields.io/badge/Auth-RFID%20%2B%20Face-success?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Field%20Ready-brightgreen?style=for-the-badge)

An automated attendance system that combines RFID identification with real-time facial recognition. A card tap triggers identity verification via webcam, and the result is logged to a local database — no manual entry required.

---
## 📑 Documentation
| Document | Description |
|----------|-------------|
| [README.md](./README.md) | Project overview, setup, and usage |
| [Report.md](./Report.md) | Linear Algebra pipeline — matrix representation, normalisation, orthogonal projection |
---
## How It Works

```
Tap RFID card
    ↓
Arduino reads Name + SRN from card
    ↓
Data sent to Python over Serial
    ↓
Webcam captures live face
    ↓
Matrix pipeline preprocesses both images
    ↓
DeepFace verifies against stored reference photo
    ↓
Result logged to SQLite database
    ↓
Arduino responds via OLED + LED + buzzer
```

---

## Hardware

- Arduino Uno R3
- MFRC522 RFID Reader + cards
- SH1106 OLED Display (I2C, 128×64)
- Red, Green, Blue LEDs
- Passive buzzer
- Laptop webcam

---

## Wiring

**RFID (MFRC522 → Arduino)**
```
SDA  → D10
SCK  → D13
MOSI → D11
MISO → D12
RST  → D7
VCC  → 3.3V
GND  → GND
```

**OLED (SH1106, I2C)**
```
VCC → 5V
GND → GND
SCL → A5
SDA → A4
```

**LEDs + Buzzer**
```
Red LED   → D6
Green LED → D5
Blue LED  → D3
Buzzer    → D9
```

**To view circuit: [Click here to view on Wokwi](https://wokwi.com/projects/461017505950764033)**

<img width="1545" height="1030" alt="Screenshot 2026-04-11 at 8 30 59 PM" src="https://github.com/user-attachments/assets/6762d7cc-4d0a-4c5b-801f-c97f13befa61" />

---

## Software Stack

| Library | Role |
|---|---|
| Python 3.11 | Core backend runtime |
| OpenCV | Webcam capture and grayscale image processing |
| DeepFace (FaceNet512) | Face verification — compares live capture against stored reference |
| NumPy | Matrix operations for the image preprocessing pipeline |
| PySerial | Two-way serial communication with the Arduino |
| SQLite | Local attendance database — no external server needed |
| Arduino IDE | Compiling and flashing the `.ino` to the Uno |

### Face Verification Pipeline

Verification runs in two stages per scan:

1. **Matrix projection** — both images are resized to 64×64, flattened into vectors, normalized, and compared via dot product projection. Produces a similarity score used for logging.
2. **DeepFace (FaceNet512)** — full deep learning verification using cosine distance. A distance below `0.40` marks the scan as `Present`, anything above is `Rejected`.

Both results are stored in the database for every scan.

### Serial Communication

Arduino and Python communicate over Serial at 9600 baud using a simple two-way protocol:

- On startup, Python sends `PING` — Arduino responds with `READY` and turns on the blue LED
- On card tap, Arduino sends `Name,SRN` — Python processes and replies with `Present` or `Rejected`
- Arduino waits up to 15 seconds for a reply before timing out

---

## Project Structure

```
smart-attendance-system/
│
├── src/
│   ├── main.py            # Entry point — orchestrates the full pipeline
│   ├── serial_reader.py   # Arduino ↔ Python serial communication
│   ├── face_match.py      # Matrix preprocessing and projection similarity
│   ├── attendance_db.py   # SQLite read/write
│   └── config.py          # Ports, paths, thresholds
│
├── hardware/
│   └── arduino.ino        # RFID read, OLED display, LED and buzzer control
│
├── student_db/            # Reference images, named by SRN
├── captures/              # Live captures saved per scan
├── data/
│   └── attendance.db
│
├── requirements.txt
└── README.md
```

---

## Setup

**1. Virtual environment**
```bash
python -m venv venv
venv\Scripts\activate
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

> On Windows, use Python 3.11 and a short project path. Long paths (e.g. inside iCloud/OneDrive) will cause `dlib` to fail during build.

**3. Flash Arduino**

Open `hardware/arduino.ino` in Arduino IDE and upload to the Uno.

**4. Add reference images**

Place photos in `student_db/` named by SRN:
```
student_db/
├── PES1UG24CS901.jpg
├── PES1UG24CS151.jpg
└── ...
```

**5. Set COM port**

Update `src/config.py`:
```python
SERIAL_PORT = "COM3"
```

**6. Run**
```bash
python src/main.py
```

> First run will download the FaceNet512 model — this is a one-time process.

---

## Attendance Record

| Field | Description |
|---|---|
| SRN | Student registration number |
| Name | Read from RFID card |
| Timestamp | Date and time of scan |
| Photo Path | Path to captured image |
| Confidence | DeepFace similarity score |
| Status | `Present` or `Rejected` |

---

## LED Reference

| LED | State |
|---|---|
| Blue | Idle — waiting for card |
| Green | Verified — attendance marked |
| Red | Mismatch or error |

---

## Author
**Vivian Sobers E**
