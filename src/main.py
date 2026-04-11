import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["ABSL_MIN_LOG_LEVEL"] = "3"

import warnings
warnings.filterwarnings("ignore")

import logging
logging.getLogger("tensorflow").setLevel(logging.ERROR)
logging.getLogger("absl").setLevel(logging.ERROR)

import cv2
from datetime import datetime
from time import sleep
from deepface import DeepFace

from attendance_db import init_db, insert_attendance
from serial_reader import RFIDSerial
from config import *
from face_match import (
    image_to_matrix,
    matrix_to_vector,
    normalize_vector,
    projection_similarity
)
os.makedirs(CAPTURES, exist_ok=True)
os.makedirs("data", exist_ok=True)

def capture_live_image(srn):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(
        CAPTURES,
        f"{srn}_{timestamp}.jpg"
    )
    cap = cv2.VideoCapture(CAMERA_INDEX)
    if not cap.isOpened():
        print("[Camera] Failed to open")
        return None
    sleep(0.5)
    ret, frame = cap.read()
    cap.release()
    if not ret or frame is None:
        print("[Camera] Capture failed")
        return None
    cv2.imwrite(path, frame)
    print(f"[Camera] Saved: {path}")
    return path


def verify_face(ref_path, live_path):
    result = DeepFace.verify(
        img1_path=ref_path,
        img2_path=live_path,
        model_name="Facenet512",
        detector_backend="opencv",
        enforce_detection=False
    )
    distance = round(result["distance"], 4)
    status = "Present" if distance < 0.50 else "Rejected"
    return status, distance

def process_attendance(rfid):
    name, srn = rfid.read_rfid()
    if not name or not srn:
        return
    print("\n" + "=" * 45)
    print(f"[RFID] {name} | {srn}")
    ref_path = os.path.join(
        STUDENT_DB,
        f"{srn}.jpg"
    )
    if not os.path.exists(ref_path):
        print("[DB] Reference image missing")
        rfid.send_result("Rejected")
        return

    live_path = capture_live_image(srn)
    if not live_path:
        rfid.send_result("Rejected")
        return
    ref_matrix = image_to_matrix(ref_path)
    live_matrix = image_to_matrix(live_path)
    ref_vec = normalize_vector(
        matrix_to_vector(ref_matrix)
    )
    live_vec = normalize_vector(
        matrix_to_vector(live_matrix)
    )
    matrix_score = projection_similarity(
        ref_vec,
        live_vec
    )
    print(f"[Matrix] {matrix_score:.2f}%")
    status, distance = verify_face(
        ref_path,
        live_path
    )
    print(f"[Distance] {distance}")
    print(f"[Result] {status}")
    insert_attendance(
        srn,
        name,
        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        live_path,
        matrix_score,
        status
    )
    rfid.send_result(status)
    print("=" * 45)

if __name__ == "__main__":
    print("[System] Initializing...")
    init_db()
    print("[DeepFace] Warming up...")
    DeepFace.build_model("Facenet512")
    rfid = RFIDSerial()
    print("[System] Ready — tap card")
    try:
        while True:
            process_attendance(rfid)
            sleep(0.3)
    except KeyboardInterrupt:
        print("\n[System] Stopped")
        rfid.close()