// (c) Tony Yan 2017
#include <Servo.h>
Servo hand, arm, wrist, elbowL, elbowR, base, temp;
int led = 8;
int buzzer = 9;
int potHand = 1;
int potWrist = 2;
int potArm = 3;
int potMuscle = 4;
int potBase = 5;

int incoming[5];

float valWrist, valArm, valMuscleL, valMuscleR, valBase;
float posElbow,posArm, posWrist, posBase, posHand;
int valHand = 90;

void setup()
{
    posElbow = 90;
    posArm = 90;
    posWrist = 90;
    posBase = 90;
    hand.attach(2);
    wrist.attach(3);
    arm.attach(4);
    elbowL.attach(5);
    elbowR.attach(6);
    base.attach(7);
    pinMode(led, OUTPUT);
    pinMode(buzzer, OUTPUT);
    Serial.begin(250000);
    Serial.write("1");

}

int mode = 2;
void loop()
{
    digitalWrite(led, LOW);
    
    while (Serial.available() >= 6)
    {
        // fill array
        // array: hand, wrist, arm, elbow, base
        for (int i = 0; i < 6; i++)
        {
            incoming[i] = Serial.read();
        }
        mode = incoming[5];
        if (mode == 1){
            posHand = incoming[0];
            posWrist = incoming[1];
            posArm = incoming[2];
            posElbow = incoming[3];
            posBase = incoming[4];
            noTone(buzzer);
        }
        
    }
    if (mode = 0){
        tone(buzzer, 1000);
    }
    if (mode == 2){
        noTone(buzzer);
        digitalWrite(led, HIGH);
        valHand = analogRead(potHand);
        posHand = map(valHand, 0, 1023, 0, 180);

        valWrist = analogRead(potWrist);
        valWrist = map(valWrist, 0, 1023, -30,32);
        if (valWrist > 0 && posWrist < 180){
          posWrist += valWrist*0.05;
        }
        if (valWrist < 0 && posWrist > 0){
          posWrist += valWrist*0.05;
        }
        valArm = analogRead(potArm);
        valArm = map(valArm, 0, 1023, -30,32);
        if (valArm > 0 && posArm < 180){
          posArm += valArm*0.03;
        }
        if (valArm < 0 && posArm > 0){
          posArm += valArm*0.03;
        }
        valMuscleL = analogRead(potMuscle);
        valMuscleL = map(valMuscleL, 0, 1023, -32,32);
        if (valMuscleL > 0 && posElbow < 180){
          posElbow += valMuscleL*0.03;
        }
        if (valMuscleL < 0 && posElbow > 0){
          posElbow += valMuscleL*0.03;
        }
        valBase = analogRead(potBase);
        valBase = map(valBase, 0, 1023, -30,32);
        if (valBase > 0 && posBase < 180){
          posBase += valBase*0.03;
        }
        if (valBase < 0 && posBase > 0){
          posBase += valBase*0.03;
        }
        delay(10);
    }
    hand.write(posHand);
    wrist.write(int(posWrist));
    arm.write(int(posArm));
    elbowL.write(int(posElbow));
    elbowR.write(int(180-posElbow));
    base.write(int(posBase));
    
}
