import tkinter as tk
import customtkinter as ctk
import cv2
import time
from PIL import Image
from multiprocessing import Queue, Process
from Unified_Detection import UnifiedDetect
from queue import Empty
import socket
import serial

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class MyApp(ctk.CTk):
    def __init__(self, label_queue, output_queue, p1, p2, p3):
        super().__init__()
        self.find_center()
        self.title("🔐 AI-Powered Door Security")
        self.geometry(f"{self.width - 200}x{self.height - 100}+{self.center_x}+{self.center_y}")
        self.resizable(False, False)
        self.configure(fg_color="#1e1e1e")

        self.label_queue = label_queue
        self.output_queue = output_queue

        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

        self.build_gui()
        self.update_gui()

    def find_center(self):
        self.width = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()
        self.center_x = int((self.width / 2 - (self.width - 200) / 2))
        self.center_y = int((self.height / 2 - (self.height - 100) / 2))

    def update_gui(self):
        updated = False
        try:
            frame_data = self.output_queue.get_nowait()
            frame = cv2.cvtColor(frame_data[0], cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            now = time.time()
            delay = now - frame_data[1]
            print(f"Frame Lag: {delay:.3f} seconds")
            img = img.resize((640, 480))
            ctk_img = ctk.CTkImage(light_image=img, size=(640, 480))
            self.cam_label.configure(image=ctk_img)
            self.cam_label.image = ctk_img
            updated = True
        except Empty:
            pass

        try:
            labels = self.label_queue.get_nowait()
            self.f_label.configure(text=f"👤 Face: {labels[0]}")
            arms = labels[1]
            self.w_label.configure(text=f"🔫 Arms: {arms.split()[0] if arms else 'None'}")
            updated = True
        except Empty:
            pass

        delay = 100 if not updated else 30
        self.after(delay, self.update_gui)

    def on_closing(self):
        self.destroy()
        self.p1.terminate()
        self.p2.terminate()
        self.p3.terminate()

    def build_gui(self):
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # === Header ===
        img1 = Image.open("data/images/door_lock.png")
        img1 = ctk.CTkImage(light_image=img1, size=(60, 60))

        self.header = ctk.CTkFrame(self, fg_color="#2c2f33", corner_radius=0, height=70)
        self.header.pack(fill="x", padx=0, pady=0)

        ctk.CTkLabel(self.header, text="  AI Powered Door Security", image=img1,
                     compound="left", font=("Segoe UI", 30, "bold"),
                     text_color="#ffffff", fg_color="#2c2f33").pack(side="left", padx=20)

        # === Main Layout ===
        self.main = ctk.CTkFrame(self, fg_color="#1e1e1e")
        self.main.pack(fill="both", expand=True)

        # === Left Info Panel ===
        self.info_frame = ctk.CTkFrame(self.main, fg_color="#2c2f33", width=280, corner_radius=10)
        self.info_frame.pack(side="left", fill="y", padx=(20, 10), pady=20)
        self.info_frame.pack_propagate(False)

        self.f_label = ctk.CTkLabel(self.info_frame, text="👤 Face: --", font=("Segoe UI", 18),
                                    text_color="white", anchor="w")
        self.f_label.pack(anchor="w", padx=20, pady=(30, 10))

        self.w_label = ctk.CTkLabel(self.info_frame, text="🔫 Arms: --", font=("Segoe UI", 18),
                                    text_color="white", anchor="w")
        self.w_label.pack(anchor="w", padx=20, pady=(10, 30))

        self.log_title = ctk.CTkLabel(self.info_frame, text="📋 Logs", font=("Segoe UI", 20, "bold"),
                                      text_color="#00c8ff", anchor="w")
        self.log_title.pack(anchor="w", padx=20, pady=(10, 5))

        self.log_frame = ctk.CTkFrame(self.info_frame, fg_color="#1e1e1e", corner_radius=8, height=200)
        self.log_frame.pack(fill="both", expand=False, padx=15, pady=(0, 20))

        # === Right Camera View ===
        self.cam_frame = ctk.CTkFrame(self.main, fg_color="#2c2f33", corner_radius=10)
        self.cam_frame.pack(side="left", fill="both", expand=True, padx=(10, 20), pady=20)
        self.cam_frame.pack_propagate(False)

        self.cam_label = ctk.CTkLabel(self.cam_frame, text="", width=640, height=480,
                                      fg_color="#000000", corner_radius=10)
        self.cam_label.pack(expand=True, padx=20, pady=20)


# === TCP Server for ESP8266 Trigger (optional) ===
def start_tcp_server(label_queue):
    print("📡 Sender Ready. Waiting for labels to send to ESP8266...")

    ESP8266_IP = "192.168.1.100"
    ESP8266_PORT = 5000

    while True:
        label = label_queue.get(timeout=0.01)
        try:
            print(f"📦 Sending label to ESP8266: {label}")
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((ESP8266_IP, ESP8266_PORT))
            client_socket.sendall(str(label).encode())
            client_socket.close()
            print("✅ Label sent successfully.\n")
        except Exception as e:
            print(f"❌ Error sending label: {e}")
            time.sleep(2)

def send_label_over_serial(label_queue):
    print("📡 Sender Ready. Waiting for labels to send to Arduino Uno...")

    # 👇 Change COM port according to your PC (Check in Device Manager)
    SERIAL_PORT = "COM10"      # Example: COM3, COM4, COM5 etc.
    BAUD_RATE = 9600          # Must match Arduino's Serial.begin(9600)

    try:
        arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)  # Wait for Arduino to fully reset
        print(f"✅ Connected to {SERIAL_PORT}")
    except Exception as e:
        print(f"❌ Couldn't open serial port: {e}")
        return

    while True:
        try:
            label = label_queue.get(timeout=0.01)
            if label:
                print(f"📦 Sending label to Arduino: {label}")
                arduino.write((str(label) + "\n").encode())
                print("✅ Label sent successfully.\n")
        except Empty:
            continue
        except Exception as e:
            print(f"❌ Error while sending label: {e}")
            break

def start_detection():
    label_queue = Queue()
    output_queue = Queue()
    trigger_queue = Queue()

    detection = UnifiedDetect()

    p1 = Process(target=detection.unified_detection_fn, args=(label_queue, output_queue, trigger_queue))
    p2 = Process(target=detection.speak, args=(label_queue,))
    p3 = Process(target=send_label_over_serial, args=(label_queue, ))

    p1.start()
    p2.start()
    p3.start()

    app = MyApp(label_queue, output_queue, p1, p2, p3)
    app.mainloop()
if __name__ == "__main__":
    start_detection()
