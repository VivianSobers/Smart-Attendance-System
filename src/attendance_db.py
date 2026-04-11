import sqlite3
import os

DB_PATH = os.path.join("data", "attendance.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        srn TEXT NOT NULL,
        name TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        photo_path TEXT NOT NULL,
        confidence REAL NOT NULL,
        status TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()


def insert_attendance(srn, name, timestamp, photo_path, confidence, status):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO attendance
    (srn, name, timestamp, photo_path, confidence, status)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        srn,
        name,
        timestamp,
        photo_path,
        confidence,
        status
    ))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print("Database initialized")