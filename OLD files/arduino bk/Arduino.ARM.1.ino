// (c) Tony Yan 2017

#include <Servo.h>

Servo hand, arm, wrist, muscleL, muscleR, base, temp;
int led = 8;

int valHand = 90;
float valWrist, valArm, valMuscleL, valMuscleR, valBase;
float posWrist, posArm, posMuscle, posBase;

void setup() {
  hand.attach(2);
  wrist.attach(3);
  arm.attach(4);
  muscleL.attach(5);
  muscleR.attach(6);
  base.attach(7);
  pinMode(led, OUTPUT);

  Serial.begin(9600); 
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }

}


void loop() {
float posMuscle = 90;
float posArm = 90;
float posWrist = 90;
float posBase = 90;

  for (;;) {
    digitalWrite(led, HIGH);
    delay(10);    
    digitalWrite(led, LOW);
    delay(10);    
    }
}


