**AI-Powered Door Security**

AI-Powered Door Security is a hardware + software prototype that demonstrates real-time door-security features using a combo of microcontrollers and AI:

Weapon detection with YOLOv8 (object detection)

Face detection / recognition with dlib

Local hardware controls via Arduino Uno (serial) and ESP8266 (Wi-Fi)

Extra sensors: ultrasonic (presence detection), buzzer & LEDs for alerts

This repo is a sample/demo to show how edge devices + AI models can work together for door access & alerting. Use it responsibly — it’s a prototype, not a certified security product.

**🔥 Highlights / What it does**

Detects weapons in camera frames using YOLOv8 and raises alerts.

Runs a face recognition check (dlib) to optionally allow/deny access.

If threat detected → triggers buzzer/LED and sends signal to Arduino/ESP8266.

Uses ultrasonic sensor to conserve compute (only run camera inference when someone is near).

Supports both serial (USB) and Wi-Fi communication between the AI host and microcontrollers.

**🧰 Tech Stack & Components**

**Software**

Python 3.11+

Ultralytics YOLOv8 (for object / weapon detection)

dlib (face detection / recognition)

OpenCV (video capture + image ops)

PySerial (serial comms to Arduino)

requests / sockets (for ESP8266 HTTP/WebSocket comms)

**Hardware**

Arduino Uno

ESP8266 (e.g. NodeMCU or ESP-01) for Wi-Fi signalling

HC-SR04 Ultrasonic distance sensor

Buzzer (active)

LEDs (status)

Webcam (or Pi Camera) on the AI host machine
