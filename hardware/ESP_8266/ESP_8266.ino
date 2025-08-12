#include <ESP8266WiFi.h>

// GPIO Pins
#define trigPin 14     // D5 = GPIO14
#define echoPin 12     // D6 = GPIO12
#define redLedPin 2    // D4 = GPIO2 (built-in RED LED)
#define buzzerPin 0    // D3 = GPIO0
#define greenLedPin 4  // D2 = GPIO4 (GREEN LED)

const char* ssid = "GBH-05";
const char* password = "456786456";

// TCP server IP and port
WiFiServer server(5000);  // Python will connect here

void setup() {
  Serial.begin(9600);

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(redLedPin, OUTPUT);
  pinMode(buzzerPin, OUTPUT);
  pinMode(greenLedPin, OUTPUT);

  digitalWrite(redLedPin, HIGH);   // OFF (inverted)
  digitalWrite(buzzerPin, LOW);    // OFF
  digitalWrite(greenLedPin, LOW);  // OFF

  connectWiFi();
  server.begin();
  Serial.println("✅ ESP Ready. Waiting for label...");
}

void loop() {
  checkDistanceForGreenLED();  // Green LED logic
  checkForPythonLabel();       // Wait for labels from Python
  delay(100);                  // Short delay to avoid flooding
}

void connectWiFi() {
  Serial.print("Connecting to WiFi");
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\n✅ WiFi connected!");
  Serial.print("📡 ESP IP: ");
  Serial.println(WiFi.localIP());
}

void checkDistanceForGreenLED() {
  int distance = measureDistance();
  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println(" cm");

  if (distance >= 20 && distance <= 70) {
    digitalWrite(greenLedPin, HIGH);  // 🟢 Green ON
  } else {
    digitalWrite(greenLedPin, LOW);  // 🟢 Green OFF
  }
}

void checkForPythonLabel() {
  WiFiClient client = server.available();
  if (client) {
    Serial.println("📥 Python app connected...");

    String received = "";
    unsigned long timeout = millis();

    while (client.connected() && millis() - timeout < 3000) {
      while (client.available()) {
        char c = client.read();
        received += c;
        timeout = millis();  // Reset timeout on activity
      }
    }

    client.stop();
    received.trim();
    Serial.println("🔍 Received label: " + received);

    // Trigger red LED + buzzer on label
    if (received.indexOf("unknown") >= 0 || received.indexOf("guns") >= 0 || received.indexOf("knife") >= 0) {
      triggerAlert();  // 🚨 Trigger buzzer + red LED
    }
  }
}

void triggerAlert() {
  for (int i = 0; i < 5; i++) {
    digitalWrite(redLedPin, LOW);   // 🔴 Red ON
    digitalWrite(buzzerPin, HIGH);  // 🔊 Buzzer ON
    delay(200);
    digitalWrite(redLedPin, HIGH);  // 🔴 Red OFF
    digitalWrite(buzzerPin, LOW);   // 🔊 Buzzer OFF
    delay(200);
  }
}

int measureDistance() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  long duration = pulseIn(echoPin, HIGH, 30000);  // Timeout 30ms
  if (duration == 0) return -1;

  return duration * 0.0343 / 2.0;
}
