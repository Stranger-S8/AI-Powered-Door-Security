import face_recognition
import cv2
import os
import pickle
import pyttsx3

class FaceDetect:

    def __init__(self):
        self.path = "known_faces"
        self.known_face_encodings = []
        self.known_face_names = []


        if not os.path.exists(self.path) or not os.listdir(self.path):
            print("No Known Faces Found. Make Sure the 'known_faces' folder has images")
            exit(0)

        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 1)

    def load_data_pickle(self):
        try:
            with open("data/face_encodings/encodings.pkl", "rb") as f:
                self.known_face_encodings, self.known_face_names = pickle.load(f)
            return True
        except FileExistsError:
            print("File Not Found")
            return False

    def store_encodings(self, images):
        result = self.load_data_pickle()
        if result:
            os.remove("data/face_encodings/encodings.pkl")

        for file_name in os.listdir(images):
            image_path = os.path.join(images, file_name)
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)
            if encodings:
                self.known_face_encodings.append(encodings[0])
                self.known_face_names.append(os.path.splitext(file_name)[0])
            else:
                print(f"Face not Found in {file_name}")

            with open("data/face_encodings/encodings.pkl", "wb") as f:
                pickle.dump((self.known_face_encodings, self.known_face_names), f)

            print("Encodings Saved Successfully")

    def detect_faces(self):
        if not os.path.exists("data/face_encodings/encodings.pkl"):
            print("No Encodings Found")
            exit(1)

        with open("data/face_encodings/encodings.pkl", "rb") as f:
            self.known_face_encodings, self.known_face_names = pickle.load(f)
        video_capture = cv2.VideoCapture(0)
        if not video_capture.isOpened():
            print("WebCam Not Detected")
            exit()

        print("Starting Face Recognition. Press 'q' to quit")

        while True:
            ret, frame = video_capture.read()
            if not ret:
                print("Failed to grab Frame")
                break

            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            print(f"Found {len(face_locations)} face(s)")

            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                name = "Unknown"

                if True in matches:
                    match_index = matches.index(True)
                    name = self.known_face_names[match_index]

                    self.engine.say(name)


                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

            cv2.imshow("Face Recognition", frame)

            if cv2.waitKey(1) == ord('q'):
                break
        video_capture.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    App = FaceDetect()
    # App.store_encodings()
    App.detect_faces()

