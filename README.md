# AI-Powered Door Security

A hardware + software prototype demonstrating real-time door-security workflows using computer vision + microcontrollers.

## Overview

This project combines:

- Weapon/object detection
- Face detection / recognition
- Optional voice interaction modules
- Local hardware control via Arduino UNO + ESP8266 (LED/buzzer/sensors)

## Getting Started

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python Application.py
```

## Configuration (Important)

- Do **not** commit real WiFi credentials, passwords, API keys, private keys, or biometric data.
- The ESP8266 sketch should use placeholders for WiFi credentials; keep your real values only on your machine.

## GitHub Notes

If you have model weights or other large artifacts, store them with Git LFS or publish them as releases instead of committing large binaries directly.
