import cv2
import os
import numpy as np
import pickle

dataset_path = "dataset"

faces = []
labels = []

label_map = {}

label_id = 0

for student in os.listdir(dataset_path):

    student_folder = os.path.join(dataset_path, student)

    if not os.path.isdir(student_folder):
        continue

    label_map[label_id] = student

    for img_name in os.listdir(student_folder):

        img_path = os.path.join(student_folder, img_name)

        # ignore non-image files
        if not img_name.lower().endswith((".jpg",".png",".jpeg")):
            continue

        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

        if img is None:
            continue

        # resize image for better LBPH training
        img = cv2.resize(img,(200,200))

        faces.append(img)
        labels.append(label_id)

    print("Loaded images for PRN:", student)

    label_id += 1


# check if dataset is empty
if len(faces) == 0:
    print("Dataset empty. Capture faces first.")
    exit()


recognizer = cv2.face.LBPHFaceRecognizer_create()

recognizer.train(faces, np.array(labels))

os.makedirs("model", exist_ok=True)

recognizer.save("model/face_model.yml")

# save label map
with open("model/labels.pkl","wb") as f:
    pickle.dump(label_map,f)

print("Model trained successfully")
print("Total faces used:", len(faces))