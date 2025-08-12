import face_recognition
import cv2
import os
import pickle
import numpy as np

class FaceDetect:

    def __init__(self):
        self.path = "data/known_faces"
        self.encodings_path = "data/face_encodings/encodings.pkl"
        self.known_face_encodings = []
        self.known_face_names = []

        self._validate_known_faces()
        self._load_encodings()

    def _validate_known_faces(self):
        if not os.path.exists(self.path) or not os.listdir(self.path):
            raise FileNotFoundError("No Known Faces Found. Make Sure the 'known_faces' folder has images")

    def _load_encodings(self):
        if not os.path.exists(self.encodings_path):
            raise FileNotFoundError("No Encodings Found")

        with open(self.encodings_path, "rb") as f:
            self.known_face_encodings, self.known_face_names = pickle.load(f)

    def store_encodings(self, images):
        if os.path.exists(self.encodings_path):
            os.remove(self.encodings_path)

        for file_name in os.listdir(images):
            image_path = os.path.join(images, file_name)
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)
            if encodings:
                self.known_face_encodings.append(encodings[0])
                self.known_face_names.append(os.path.splitext(file_name)[0])
            else:
                print(f"⚠️ Face not found in: {file_name}")

        os.makedirs(os.path.dirname(self.encodings_path), exist_ok=True)
        with open(self.encodings_path, "wb") as f:
            pickle.dump((self.known_face_encodings, self.known_face_names), f)

        print("✅ Encodings Saved Successfully")

    def detect_faces(self, frame, process_frame=True):
        if not process_frame:
            return frame, None

        name = "unknown"

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_small_frame)

        if not face_locations:
            return frame, None
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        print(f"Found {len(face_locations)} face(s)")

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)

            if True in matches:
                match_index = matches.index(True)
                name = self.known_face_names[match_index]

            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

        return frame, name

if __name__ == "__main__":
    app = FaceDetect()
    app.store_encodings("data/known_faces")
