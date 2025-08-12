from ultralytics import YOLO
import cv2

# Load YOLOv8 model
model = YOLO("yolov5su.pt")  # or any YOLOv8 model like 'yolov8n.pt'

# Start webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Run YOLO detection
    results = model(frame)

    # Render results using YOLOv8 format
    frame = results[0].plot()

    # Show frame
    cv2.imshow("YOLOv8 Object Detection", frame)

    # Exit on 'q' press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
