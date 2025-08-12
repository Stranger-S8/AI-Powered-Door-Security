// Pin Configuration
#define trigPin 9       // Trigger pin of ultrasonic
#define echoPin 10      // Echo pin of ultrasonic

// Direct port control pins
#define redLedPin 2     // Red LED pin (PD2)
#define greenLedPin 3   // Green LED pin (PD3)
#define buzzerPin 4     // Buzzer pin (PD4)

void setup() {
  Serial.begin(9600);  // Start serial communication

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  pinMode(redLedPin, OUTPUT);
  pinMode(greenLedPin, OUTPUT);
  pinMode(buzzerPin, OUTPUT);

  // Turn everything OFF
  PORTD &= ~((1 << PD2) | (1 << PD3) | (1 << PD4));  // Direct port write

  Serial.println("✅ Arduino Ready. Waiting for Python input...");
}

void loop() {
  checkDistanceForGreenLED();  // Handle distance sensor logic
  checkForPythonLabel();       // Handle serial communication with Python
  delay(200);                  // Delay is okay here
}

void checkDistanceForGreenLED() {
  int distance = measureDistance();

  if (distance != -1) {
    Serial.print("📏 Distance: ");
    Serial.print(distance);
    Serial.println(" cm");

    if (distance >= 20 && distance <= 70) {
      // Turn ON green LED (PD3)
      asm volatile("sbi %[port], %[pin]" :: [port] "I" (_SFR_IO_ADDR(PORTD)), [pin] "I" (3));
    } else {
      // Turn OFF green LED
      asm volatile("cbi %[port], %[pin]" :: [port] "I" (_SFR_IO_ADDR(PORTD)), [pin] "I" (3));
    }
  } else {
    Serial.println("⚠️ Distance read failed (no echo received)");
    // Turn OFF green LED
    asm volatile("cbi %[port], %[pin]" :: [port] "I" (_SFR_IO_ADDR(PORTD)), [pin] "I" (3));
  }
}

void checkForPythonLabel() {
  if (Serial.available()) {
    String received = Serial.readStringUntil('\n');
    received.trim();

    Serial.print("📥 Received from Python: ");
    Serial.println(received);

    if (received.indexOf("unknown") >= 0 || 
        received.indexOf("guns") >= 0 || 
        received.indexOf("knife") >= 0) {
      triggerAlert();  // 🚨 Alert if label matches
    }
  }
}

void triggerAlert() {
  for (int i = 0; i < 5; i++) {
    // Turn ON red LED (PD2) and Buzzer (PD4)
    asm volatile("sbi %[port], %[pin]" :: [port] "I" (_SFR_IO_ADDR(PORTD)), [pin] "I" (2));
    asm volatile("sbi %[port], %[pin]" :: [port] "I" (_SFR_IO_ADDR(PORTD)), [pin] "I" (4));
    delay(200);

    // Turn OFF both
    asm volatile("cbi %[port], %[pin]" :: [port] "I" (_SFR_IO_ADDR(PORTD)), [pin] "I" (2));
    asm volatile("cbi %[port], %[pin]" :: [port] "I" (_SFR_IO_ADDR(PORTD)), [pin] "I" (4));
    delay(200);
  }
}

int measureDistance() {
  // Clear previous pulse
  digitalWrite(trigPin, LOW);

  // Replace delayMicroseconds(2) with NOPs (about 2us = 32 cycles)
  asm volatile (
    "nop\n\t""nop\n\t""nop\n\t""nop\n\t"
    "nop\n\t""nop\n\t""nop\n\t""nop\n\t"
    "nop\n\t""nop\n\t""nop\n\t""nop\n\t"
    "nop\n\t""nop\n\t""nop\n\t""nop\n\t"
    "nop\n\t""nop\n\t""nop\n\t""nop\n\t"
    "nop\n\t""nop\n\t""nop\n\t""nop\n\t"
    "nop\n\t""nop\n\t""nop\n\t""nop\n\t"
    "nop\n\t""nop\n\t""nop\n\t""nop\n\t"
  );

  // Send 10us pulse to trigger
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Listen for echo. Timeout after 30ms.
  long duration = pulseIn(echoPin, HIGH, 30000);
  if (duration == 0) return -1;  // No echo received

  int distance = duration * 0.0343 / 2;
  return distance;
}
