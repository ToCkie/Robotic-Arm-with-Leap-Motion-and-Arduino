# from __future__ import print_function
from time import sleep
import serial
import Leap
import sys
import thread
import time
import struct

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

list_temp_smooth = [[], [], [], [], []]
count = 0


def serOutputPre(hand, wrist, arm, elbow, base):
    try:
        ser.write(struct.pack('>BBBBB', int(hand), int(
            wrist), int(arm), int(elbow), int(base)))
    except:
        return 1
    return 0


def map(var, inL, inH, outL, outH):
    temp = (var - inL) / ((inH - inL) / ((outH - outL) * 1.0))
    if temp > outH:
        return outH
    elif temp < outL:
        return outL
    else:
        return temp


def LeapRaw(strength, confidence, hand_pitch, arm_pitch, arm_yaw):
    wrist, arm, elbow, base, hand = (
        (map(hand_pitch, 0.3, -0.2, 50, 180)),
        (map(arm_pitch, 0.4, -0.1, 80, 180)),
        (map(arm_pitch, -0.3, 0.4, 40, 105)),
        (map(arm_yaw, 0.4, -0.4, 0, 180)),
        (map(strength, 1, 0, 10, 90)))
    print "  strength:   %s \n  confidence: %s \n  hand_pitch: %s \n  arm_pitch:  %s \n  arm_yaw:    %s \n ---------------------------" % (
        strength, confidence, hand_pitch, arm_pitch, arm_yaw)
    print "    confidence: %f \n    hand:      %f \n    wrist:     %f \n    arm:       %f \n    elbow:     %f \n    base:      %f" % (confidence, hand, wrist, arm, elbow, base)

    serOutputPre(hand, wrist, arm, elbow, base)
    print('----------------------------------')


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
        print("Frame id: %d, timestamp: %d, hands: %d, fingers: %d" % (
            frame.id, frame.timestamp, len(frame.hands), len(frame.fingers)))
        counter = 0
        temp_list = []
        for hand in frame.hands:
            print(hand, counter)
            handType = "Left hand" if hand.is_left else "Right hand"
            # hand = frame.hands[0]
            normal = hand.palm_normal
            direction = hand.direction
            arm = hand.arm

            # print("  %s, id %d \n  Position: %s" % (
            #     handType, hand.id, hand.palm_position))
            # print("    Grab Strength: %s" % (hand.grab_strength))
            # print("    Confidence: %s" % (hand.confidence))
            # print("  Hand:\n    pitch: %f  \n    roll:  %f  \n    yaw:   %f " % (
            #     direction.pitch, normal.roll, direction.yaw))
            # print("  Arm direction: \n    pitch: %f  \n    yaw:   %f " % (
            #     arm.direction[1], arm.direction[0]))
            # print("  wrist position: %s \n  elbow position: %s" % (
            #     arm.wrist_position, arm.elbow_position))
            # print("")
            if counter == 0:
                counter = 1
                temp_list+=[hand.grab_strength, hand.confidence, direction.pitch]
            else:
                temp_list+=[arm.direction[1], arm.direction[0]]
                counter = 0
        # print(temp_list)
        LeapRaw(temp_list[0],temp_list[1],temp_list[2],temp_list[3],temp_list[4])


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
