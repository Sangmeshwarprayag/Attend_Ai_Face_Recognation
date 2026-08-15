import cv2
import sqlite3
import datetime
import os
from ultralytics import YOLO

# -------------------------
# Load YOLO model (optional)
# -------------------------
model = YOLO("yolov8n.pt")

# -------------------------
# Load LBPH recognizer
# -------------------------
if not os.path.exists("model/face_model.yml"):
    print("❌ Model not found! Train model first.")
    exit()

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("model/face_model.yml")

# -------------------------
# Face detector
# -------------------------
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# -------------------------
# Label mapping
# -------------------------
dataset_path = "dataset"

if not os.path.exists(dataset_path):
    print("❌ Dataset folder missing")
    exit()

label_map = {}
for i, folder in enumerate(os.listdir(dataset_path)):
    label_map[i] = folder

# -------------------------
# Database path
# -------------------------
DB_PATH = "database/attendai.db"

# -------------------------
# Start camera
# -------------------------
cam = cv2.VideoCapture(0)

if not cam.isOpened():
    print("❌ Camera not opening")
    exit()

marked_students = set()

print("✅ Attendance Camera Started")

while True:

    ret, frame = cam.read()

    if not ret:
        print("❌ Frame not captured")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:

        face_img = gray[y:y+h, x:x+w]
        face_img = cv2.resize(face_img, (200, 200))

        try:
            label, confidence = recognizer.predict(face_img)

            if confidence < 80:

                prn = label_map.get(label, "Unknown")

                # Draw box
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

                # Show name
                cv2.putText(frame, prn, (x, y-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                            (0, 255, 0), 2)

                # Mark attendance
                if prn != "Unknown" and prn not in marked_students:

                    conn = sqlite3.connect(DB_PATH)
                    cursor = conn.cursor()

                    today = datetime.date.today()

                    cursor.execute(
                        "SELECT * FROM attendance WHERE prn=? AND date=?",
                        (prn, today)
                    )

                    exists = cursor.fetchone()

                    if not exists:
                        cursor.execute(
                            "INSERT INTO attendance(prn,date,status) VALUES(?,?,?)",
                            (prn, today, "Present")
                        )

                        conn.commit()
                        print("✅ Attendance marked:", prn)

                    conn.close()

                    marked_students.add(prn)

        except Exception as e:
            print("⚠️ Error:", e)

    cv2.imshow("AttendAI Attendance Camera", frame)

    if cv2.waitKey(1) == 27:  # ESC key
        break

cam.release()
cv2.destroyAllWindows()