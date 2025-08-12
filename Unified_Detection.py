import time
from multiprocessing import Process, Queue
import cv2
from queue import Empty
from Face_Recognition import FaceDetect
from Weapon_Detection import WeaponDetect
from Speech_Recognition import RecognizeSpeech
from Additional_Features import Features

class UnifiedDetect:
    def __init__(self):
        self.video_capture = None
        self.obj1 = None
        self.obj2 = None
        self.obj3 = None
        self.obj4 = None
        self.count = 0
        self.door_pass = None

    def unified_detection_fn(self, label_queue, output_queue, trigger_queue):
        self.obj1 = FaceDetect()
        self.obj2 = WeaponDetect()
        self.cap = cv2.VideoCapture(1)

        frame_count = 0

        while True:
            ret, frame = self.cap.read()
            if ret:
                process_frame = (frame_count % 5 == 0)
                timestamp = time.time()
                frame, label1 = self.obj1.detect_faces(frame, process_frame)
                frame, label2 = self.obj2.detect_objects_from_camera(frame)
                label_queue.put((label1, label2))
                output_queue.put((frame, timestamp))
                frame_count += 1

    def listen_voice(self):
        self.obj3 = RecognizeSpeech()
        self.obj4 = Features()
        while True:
            print("Listening")

            text = self.obj3.speech_to_text()

            result = self.obj4.verify_password(text)
            if result:
                print("Password is Correct")
            else:
                print("Password is Incorrect")

    def speak(self, label_queue):
        self.obj3 = RecognizeSpeech()

        while True:
            label = label_queue.get()

            if label[0] is not None:
                if label[0] == "Unknown":
                    self.obj3.text_to_speech("Password Please")
                    self.count += 1

                self.obj3.text_to_speech(f"Face Detected : {label[0]}")
            if label[1]:
                self.obj3.text_to_speech(f"Detected : {label[1].split()[0]}")


# if __name__ == "__main__":
#     label_queue = Queue()
#
#     A = UnifiedDetect()
#
#
#     p1 = Process(target=A.unified_detection_fn, args=(label_queue, ))
#     p2 = Process(target=A.listen_voice)
#     p3 = Process(target=A.speak, args=(label_queue, ))
#
#     p1.start()
#     p2.start()
#     p3.start()
#
#     p1.join()
#     p2.join()
#     p3.join()

