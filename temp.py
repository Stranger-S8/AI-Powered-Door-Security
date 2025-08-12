import cv2

for i in range(5):
    cap = cv2.VideoCapture(i)
    ret, frame = cap.read()
    if ret:
        print(f"Camera index {i} is working!")
        cap.release()
