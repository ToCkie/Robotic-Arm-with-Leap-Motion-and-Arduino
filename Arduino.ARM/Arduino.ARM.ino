// (c) Tony Yan 2017

#include <Servo.h>

Servo hand, arm, wrist, muscleL, muscleR, base, temp;
int led = 8;

int potHand = 1;
int potWrist = 2;
int potArm = 3;
int potMuscle = 4;
int potBase = 5;

int valHand = 90;
float valWrist, valArm, valMuscleL, valMuscleR, valBase;
//float posMuscle = 90;
//float posArm = 90;
//float posWrist = 90;
//float posBase = 90;
float posMuscle,posArm, posWrist, posBase;
void setup() {
  hand.attach(2);
  wrist.attach(3);
  arm.attach(4);
  muscleL.attach(5);
  muscleR.attach(6);
  base.attach(7);
  pinMode(led, OUTPUT);
  Serial.begin(250000); 

}


void loop() {
float posMuscle = 90;
float posArm = 90;
float posWrist = 90;
float posBase = 90;
  for (;;) {
    digitalWrite(led, HIGH);
    
///////////////////////Servo: hand=2 ,potHand=1
    valHand = analogRead(potHand);
    valHand = map(valHand, 0, 1023, 0, 180);
    hand.write(valHand);
    
///////////////////////Servo: wrist=3 ,potWrist=2
    valWrist = analogRead(potWrist);
    valWrist = map(valWrist, 0, 1023, -30,32);
    if (valWrist > 0 && posWrist < 180){
      posWrist += valWrist*0.05;
    }
    if (valWrist < 0 && posWrist > 0){
      posWrist += valWrist*0.05;
    }
    wrist.write(int(posWrist));

///////////////////////Servo: arm=4 ,potArm=3
    valArm = analogRead(potArm);
    valArm = map(valArm, 0, 1023, -30,32);
    if (valArm > 0 && posArm < 180){
      posArm += valArm*0.03;
    }
    if (valArm < 0 && posArm > 0){
      posArm += valArm*0.03;
    }
    arm.write(int(posArm));

///////////////////////Servo: muscleL=5 , muscleR=6 ,potMuscle=4
    valMuscleL = analogRead(potMuscle);
    valMuscleL = map(valMuscleL, 0, 1023, -32,32);
    if (valMuscleL > 0 && posMuscle < 180){
      posMuscle += valMuscleL*0.03;
    }
    if (valMuscleL < 0 && posMuscle > 0){
      posMuscle += valMuscleL*0.03;
    }
    muscleL.write(int(posMuscle));
    muscleR.write(int(180-posMuscle));
    
///////////////////////Servo: base=7 ,potBase=5
    valBase = analogRead(potBase);
    valBase = map(valBase, 0, 1023, -30,32);
    if (valBase > 0 && posBase < 180){
      posBase += valBase*0.03;
    }
    if (valBase < 0 && posBase > 0){
      posBase += valBase*0.03;
    }
    base.write(int(posBase));



    
  //  hand.(2);wrist.(3);arm.(4); muscleL.(5); muscleR.(6);base.(7);
    //digitalWrite(led, LOW);
    
    Serial.print(" |2:");
    Serial.print(valHand);
    Serial.print(" |3:");
    Serial.print(posWrist);   
    Serial.print(" |4:");
    Serial.print(posArm); 
    Serial.print(" |5:");
    Serial.print(posMuscle);
    Serial.print(" |6:");
    Serial.print(180-posMuscle);
    Serial.print(" |7:");
    Serial.print(posBase);
   
  //  Serial.print(" ||2:");  /////////
  //  Serial.print(valWrist);
  //  Serial.print(" |3:");
  //  Serial.print(valArm);
  //  Serial.print(" |4:");
  //  Serial.print(valMuscleL);
  //  Serial.print(" |5:");
  // //  Serial.print(valBase);
     Serial.print("\n");
        
//


    delay(10);
    
    }
}


