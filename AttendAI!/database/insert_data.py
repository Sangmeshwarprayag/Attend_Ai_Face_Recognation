import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "attendai.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# STUDENTS
cursor.execute("INSERT OR IGNORE INTO students VALUES ('11111','Rahul','TYBCA','A')")
cursor.execute("INSERT OR IGNORE INTO students VALUES ('11112','Amit','TYBCA','A')")
cursor.execute("INSERT OR IGNORE INTO students VALUES ('11113','Sneha','TYBCA','B')")

# SUBJECTS
cursor.execute("INSERT OR IGNORE INTO subjects VALUES (1,'AI')")
cursor.execute("INSERT OR IGNORE INTO subjects VALUES (2,'OS')")

# LECTURES
cursor.execute("""
INSERT OR IGNORE INTO lectures(subject_id,course,division,start_time,end_time)
VALUES (1,'TYBCA','A','10:00','11:00')
""")

cursor.execute("""
INSERT OR IGNORE INTO lectures(subject_id,course,division,start_time,end_time)
VALUES (2,'SYBCA','B','11:00','12:00')
""")

# ATTENDANCE SAMPLE
cursor.execute("""
INSERT INTO attendance(prn,lecture_id,date,status)
VALUES ('11111',1,'2026-03-10','Present')
""")

cursor.execute("""
INSERT INTO attendance(prn,lecture_id,date,status)
VALUES ('11112',1,'2026-03-10','Absent')
""")

# LOGIN USERS

cursor.execute("INSERT OR IGNORE INTO users(username,password,role) VALUES ('admin','admin123','admin')")
cursor.execute("INSERT OR IGNORE INTO users(username,password,role) VALUES ('teacher1','teach123','teacher')")
cursor.execute("INSERT OR IGNORE INTO users(username,password,role) VALUES ('11111','student123','student')")


conn.commit()
conn.close()

print("Sample Data Inserted Successfully")