# from __future__ import print_function
from time import sleep
import serial
import Leap
import sys
import thread
import time
import struct
from numpy import mean

connected = False
# serport = 'COM3'
serport = '/dev/cu.wchusbserial1460'

try:
    while True:
        sleep(1)
        try:
            ser = serial.Serial(serport, 250000)
            print('Connecting')
            break
        except:
            print "Please connect to port %s" % (serport)

    while not connected:
        serin = ser.read()
        print("Connected")
        connected = True
except:
    print("cancelled by user")

##################################


def sendPos(hand, wrist, arm, elbow, base):
    try:
        print(hand, wrist, arm, elbow, base)
        ser.write(struct.pack('>BBBBB', int(hand), int(
            wrist), int(arm), int(elbow), int(base)))
        return 0
    except:
        return 1


smooth1, smooth2 = [], []
count = 0


def serOutputPre(hand, wrist, arm, elbow, base):
    try:
        print(smooth1,smooth2)
        if len(smooth1) == 0:
            smooth1 = [hand, wrist, arm, elbow, base]
        elif len(smooth2) == 0:
            smooth2 = [hand, wrist, arm, elbow, base]
        elif len(smooth1) == 5 and len(smooth2)==5:
            temp1 = [
                int(mean([smooth1[0],smooth2[0],hand])),
                int(mean([smooth1[1],smooth2[1],wrist])),
                int(mean([smooth1[2],smooth2[2],arm])),
                int(mean([smooth1[3],smooth2[3],elbow])),
                int(mean([smooth1[4],smooth2[4],base]))
            ]
            sendPos(temp1[0],temp1[1],temp1[2],temp1[3],temp1[4])
        return 0
    except:
        print('something went wrong')
        return 1


def map(var, inL, inH, outL, outH):
    temp = (var - inL) / ((inH - inL) / ((outH - outL) * 1.0))
    if temp > outH:
        return outH
    elif temp < outL:
        return outL
    else:
        return temp


def LeapRaw(strength, confidence, hand_pitch, arm_pitch1, arm_pitch2, arm_yaw):
    print('----------------------------------')
    hand, wrist, arm, elbow, base = (
        (map(strength, 1, 0, 10, 90)),
        (map(hand_pitch, 0.3, -0.3, 10, 170)),
        (map(arm_pitch1, 0.4, -0.4, 10, 170)),
        (map(arm_pitch2, -0.4, 0.4, 10, 170)),
        (map(arm_yaw, 0.3, -0.3, 5, 175)))
    print " hand:      %i    \t %f \n wrist:     %i    \t %f \n arm:       %i    \t %f \n elbow:     %i    \t %f \n base:      %i    \t %f " % (hand, strength, wrist, hand_pitch, arm, arm_pitch1, elbow, arm_pitch2, base, arm_yaw)
    serOutputPre(hand, wrist, arm, elbow, base)


class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    def on_init(self, controller):
        print("Initialized")

    def on_connect(self, controller):
        print("Connected")

    def on_disconnect(self, controller):
        print("Disconnected")

    def on_exit(self, controller):
        print("Exited")

    def on_frame(self, controller):
        frame = controller.frame()
        # if 1 == len(frame.hands):
        counter = 0
        temp_list = []
        for hand in frame.hands:
            handType = "Left hand" if hand.is_left else "Right hand"
            normal = hand.palm_normal
            direction = hand.direction
            arm = hand.arm
            if counter == 0:
                counter = 1
                temp_list += [hand.grab_strength, hand.confidence,
                              direction.pitch, arm.direction[1]]
            else:
                temp_list += [arm.direction[1], arm.direction[0]]
                counter = 0
        if len(temp_list) == 6:
            LeapRaw(temp_list[0], temp_list[1], temp_list[2],
                    temp_list[3], temp_list[4], temp_list[5])
        elif len(temp_list) == 4:
            print("I need another hand")
            sleep(0.5)


def leapM():
    listener = SampleListener()
    controller = Leap.Controller()
    controller.add_listener(listener)
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        controller.remove_listener(listener)

########################################


def control():
    while True:
        cmd = raw_input("command: ")
        if cmd == 'e':
            break
        elif cmd == 's':
            leapM()
        else:
            None


if __name__ == "__main__":
    control()
    ser.close
