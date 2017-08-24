#include <Servo.h>

Servo myservo;
int input;
void setup()
{
  myservo.attach(2);
  Serial.begin(250000);
  myservo.write(75);
}

void loop() {
  if (Serial.available() > 0) {
    input = Serial.parseInt();
    myservo.write(input);
    Serial.println(input);
    delay (1000);
  }
}

