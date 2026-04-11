#include <SPI.h>
#include <MFRC522.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SH110X.h>

#define SS_PIN 10
#define RST_PIN 7

#define BUZZER 9
#define RED_LED 6
#define GREEN_LED 5
#define BLUE_LED 3

MFRC522 rfid(SS_PIN, RST_PIN);
MFRC522::MIFARE_Key key;
Adafruit_SH1106G display(128, 64, &Wire, -1);

String readBlock(byte block) {
  byte buffer[18];
  byte size = sizeof(buffer);

  MFRC522::StatusCode status;

  status = rfid.PCD_Authenticate(
      MFRC522::PICC_CMD_MF_AUTH_KEY_A,
      block,
      &key,
      &(rfid.uid)
  );

  if (status != MFRC522::STATUS_OK) return "";

  status = rfid.MIFARE_Read(block, buffer, &size);

  if (status != MFRC522::STATUS_OK) return "";

  String text = "";

  for (int i = 0; i < 16; i++) {
    if (buffer[i] != 0 && buffer[i] != 255)
      text += char(buffer[i]);
  }

  text.trim();
  return text;
}

void showMessage(String line1, String line2 = "") {
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SH110X_WHITE);
  display.setCursor(0, 10);
  display.println(line1);
  display.setCursor(0, 30);
  display.println(line2);
  display.display();
}

void setIdle() {
  digitalWrite(RED_LED, LOW);
  digitalWrite(GREEN_LED, LOW);
  digitalWrite(BLUE_LED, HIGH);
  showMessage("Tap your card");
}

void setup() {
  Serial.begin(9600);

  pinMode(BUZZER, OUTPUT);
  pinMode(RED_LED, OUTPUT);
  pinMode(GREEN_LED, OUTPUT);
  pinMode(BLUE_LED, OUTPUT);

  SPI.begin();
  rfid.PCD_Init();

  display.begin(0x3C, true);

  for (byte i = 0; i < 6; i++)
    key.keyByte[i] = 0xFF;

  setIdle();
}

void loop() {
  if (!rfid.PICC_IsNewCardPresent()) return;
  if (!rfid.PICC_ReadCardSerial()) return;

  digitalWrite(BLUE_LED, LOW);

  String name = readBlock(1);
  String srn = readBlock(2);

  if (name.length() == 0 || srn.length() == 0) {
    showMessage("Card Error");
    return;
  }

  Serial.println(name + "," + srn);

  String result = "";
  unsigned long startTime = millis();

  while (millis() - startTime < 10000) {
    if (Serial.available()) {
      result = Serial.readStringUntil('\n');
      result.trim();
      break;
    }
  }

  if (result == "Present") {
    digitalWrite(GREEN_LED, HIGH);
    tone(BUZZER, 1000, 300);
    showMessage("Attendance", "Marked");
    delay(2000);
    digitalWrite(GREEN_LED, LOW);
  }
  else {
    digitalWrite(RED_LED, HIGH);
    tone(BUZZER, 400, 1000);
    showMessage("Mismatch");
    delay(2000);
    digitalWrite(RED_LED, LOW);
  }

  rfid.PICC_HaltA();
  rfid.PCD_StopCrypto1();

  setIdle();
}