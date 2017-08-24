// (c) Tony Yan 2017
#include <Servo.h>
Servo hand, arm, wrist, elbowL, elbowR, base, temp;
int led = 8;
float posHand, poselbow, posArm, posWrist, posBase;
void setup()
{
    hand.attach(2);
    wrist.attach(3);
    arm.attach(4);
    elbowL.attach(5);
    elbowR.attach(6);
    base.attach(7);
    pinMode(led, OUTPUT);
    Serial.begin(250000);
    Serial.write("1");
}

void loop()
{
    float posHand = 90;
    float poselbow = 90;
    float posArm = 90;
    float posWrist = 90;
    float posBase = 90;

    for (;;)
    {
        //    Serial.println("In the for loop");

        if (Serial.available() > 0)
        {
            int serialRec = Serial.parseInt();
            Serial.println(serialRec);
            posWrist = serialRec;
        }
        else
        {
            //      Serial.println("0");
        }

        //    Serial.write(int(posWrist));

        digitalWrite(led, LOW);
        hand.write(int(posHand));
        wrist.write(int(posWrist));
        arm.write(int(posArm));
        elbowL.write(int(poselbow));
        elbowR.write(int(180 - poselbow));
        base.write(int(posBase));

        //    delay(10);
    }
    void loop()
    {
        while (Serial.available() >= 5)
        {
            // fill array
            // array: hand, wrist, arm, elbow, base
            for (int i = 0; i < 5; i++)
            {
                incoming[i] = Serial.read();
            }
            hand.write(incoming[0]);
            wrist.write(incoming[1]);
            arm.write(incoming[2]);
            elbowL.write(incoming[3]);
            elbowR.write(180 - incoming[3]);
            base.write(incoming[4]);
        }
    }
}
