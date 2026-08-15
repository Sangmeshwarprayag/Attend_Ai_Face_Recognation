import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "attendai.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# ==========================
# USERS TABLE
# ==========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT UNIQUE,
password TEXT,
role TEXT
)
""")

# ==========================
# STUDENTS TABLE
# ==========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
prn TEXT PRIMARY KEY,
name TEXT NOT NULL,
course TEXT NOT NULL,
division TEXT NOT NULL
)
""")

# ==========================
# SUBJECTS TABLE
# ==========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS subjects(
subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
subject_name TEXT NOT NULL
)
""")

# ==========================
# LECTURES TABLE
# ==========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS lectures(
lecture_id INTEGER PRIMARY KEY AUTOINCREMENT,
subject_id INTEGER,
course TEXT,
division TEXT,
start_time TEXT,
end_time TEXT,
FOREIGN KEY(subject_id) REFERENCES subjects(subject_id)
)
""")

# ==========================
# ATTENDANCE TABLE (FIXED)
# ==========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance(
id INTEGER PRIMARY KEY AUTOINCREMENT,
prn TEXT NOT NULL,
lecture_id INTEGER,
date TEXT NOT NULL,
entry_time TEXT,
exit_time TEXT,
status TEXT DEFAULT 'Present',
FOREIGN KEY(prn) REFERENCES students(prn),
FOREIGN KEY(lecture_id) REFERENCES lectures(lecture_id)
)
""")

# ==========================
# INDEX (🔥 PERFORMANCE BOOST)
# ==========================
cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_attendance
ON attendance(prn, date)
""")

conn.commit()
conn.close()

print("✅ Database Created Successfully")