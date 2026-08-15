import cv2
import os
import sys

# get PRN from argument
prn = sys.argv[1]

dataset_path = f"dataset/{prn}"
os.makedirs(dataset_path, exist_ok=True)

# load face detector
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

cam = cv2.VideoCapture(0)

count = 0

print("Capturing faces for PRN:", prn)
print("Press C to capture image")

while True:

    ret, frame = cam.read()

    if not ret:
        print("Camera error")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:

        face_img = gray[y:y+h, x:x+w]
        face_img = cv2.resize(face_img, (200, 200))

        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)

    cv2.imshow("Capture Face", frame)

    # read key once
    key = cv2.waitKey(1) & 0xFF

    # press C to capture
    if key == ord('c') and len(faces) > 0:

        (x, y, w, h) = faces[0]
        face_img = gray[y:y+h, x:x+w]
        face_img = cv2.resize(face_img, (200, 200))

        count += 1

        img_path = f"{dataset_path}/{count}.jpg"
        cv2.imwrite(img_path, face_img)

        print("Captured image", count)

    # stop after 30 images
    if count >= 30:
        break

    # ESC to stop
    if key == 27:
        break

cam.release()
cv2.destroyAllWindows()

print("Face capture complete")