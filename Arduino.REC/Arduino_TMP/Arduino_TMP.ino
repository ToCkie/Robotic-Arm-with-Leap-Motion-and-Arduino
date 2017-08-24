// (c) Tony Yan 2017
#include <Servo.h>
Servo hand, arm, wrist, muscleL, muscleR, base, temp;
int led = 8;
float posHand, posMuscle,posArm, posWrist, posBase;
void setup() {
  hand.attach(2);
  wrist.attach(3);
  arm.attach(4);
  muscleL.attach(5);
  muscleR.attach(6);
  base.attach(7);
  pinMode(led, OUTPUT);
  Serial.begin(250000); 
  Serial.write("1");  
}

void loop() {
float posHand = 90;
float posMuscle = 90;
float posArm = 90;
float posWrist = 90;
float posBase = 90;

  for (;;) {
//    Serial.println("In the for loop");
    
    if (Serial.available() > 0){
      int serialRec = Serial.parseInt();
      Serial.println(serialRec);
      posWrist = serialRec;
    }else{
//      Serial.println("0");
    }
    
//    Serial.write(int(posWrist));
    
    digitalWrite(led, LOW);
    hand.write(int(posHand));
    wrist.write(int(posWrist));
    arm.write(int(posArm));
    muscleL.write(int(posMuscle));
    muscleR.write(int(180-posMuscle));
    base.write(int(posBase));

//    delay(10);
    
    }
}


