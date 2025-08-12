import cv2
from ultralytics import YOLO

class WeaponDetect:
    def __init__(self):
        self.yolo_model = YOLO('Pretrained Models/best.pt')
        # self.yolo_model.to('cuda') For GPU

    def detect_objects_from_camera(self, frame):
        small_frame = cv2.resize(frame, (640, 480))
        results = self.yolo_model(frame, stream=True)

        label = None

        for result in results:
            classes = result.names
            cls = result.boxes.cls
            conf = result.boxes.conf
            detections = result.boxes.xyxy

            for pos, detection in enumerate(detections):
                if conf[pos] >= 0.5:  # confidence threshold
                    xmin, ymin, xmax, ymax = detection
                    label = f"{classes[int(cls[pos])]} {conf[pos]:.2f}"
                    color = (0, int(cls[pos] * 40) % 256, 255)
                    cv2.rectangle(frame, (int(xmin), int(ymin)), (int(xmax), int(ymax)), color, 2)
                    cv2.putText(frame, label, (int(xmin), int(ymin) - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        return frame, label

# Run it directly
if __name__ == "__main__":
    A = WeaponDetect()
    # A.detect_objects_from_camera()
