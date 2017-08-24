# from __future__ import print_function
from time import sleep
import serial
import Leap
import sys
import thread
import time
import struct
import numpy
import math
import csv

connected = False
# serport = 'COM3'
serport = '/dev/cu.wchusbserial1440'

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
    # print(hand, wrist, arm, elbow, base)
    # print('----------------------------------')
    # print "    hand:      %i \n    wrist:     %i \n    arm:       %i \n    elbow:     %i \n    base:      %i" % (hand, wrist, arm, elbow, base)
    try:
        ser.write(struct.pack('>BBBBB', int(hand), int(
            wrist), int(arm), int(elbow), int(base)))
        return 0
    except:
        return 1


smooth1, smooth2, smooth3, smooth4 = [], [], [], []


def serSmooth(hand, wrist, arm, elbow, base):
    global smooth1
    global smooth2
    global smooth3
    global smooth4
    if len(smooth1) == 0:
        smooth1 = [hand, wrist, arm, elbow, base]
    elif len(smooth2) == 0:
        smooth2 = [hand, wrist, arm, elbow, base]
    elif len(smooth3) == 0:
        smooth3 = [hand, wrist, arm, elbow, base]
    elif len(smooth4) == 0:
        smooth4 = [hand, wrist, arm, elbow, base]
    elif len(smooth1) == 5 and len(smooth2) == 5 and len(smooth3) == 5 and len(smooth4) == 5:
        temp1 = [
            int(numpy.mean([smooth1[0], smooth2[0],
                            smooth3[0], smooth4[0], hand])),
            int(numpy.mean([smooth1[1], smooth2[1],
                            smooth3[1], smooth4[1], wrist])),
            int(numpy.mean([smooth1[2], smooth2[2],
                            smooth3[2], smooth4[2], arm])),
            int(numpy.mean([smooth1[3], smooth2[3],
                            smooth3[3], smooth4[3], elbow])),
            int(numpy.mean([smooth1[4], smooth2[4],
                            smooth3[4], smooth4[4], base]))
        ]
        sendPos(temp1[0], temp1[1], temp1[2], temp1[3], temp1[4])
        smooth1, smooth2, smooth3, smooth4 = [], [], [], []
    return 0


def map(var, inL, inH, outL, outH):
    temp = (var - inL) / ((inH - inL) / ((outH - outL) * 1.0))
    if temp > outH:
        return outH
    elif temp < outL:
        return outL
    else:
        return temp


def LeapRaw(handPosX, handPosYRaw, handPosZ, grab, hand_pitch):
    print("-----------------------")
    handPosY = handPosYRaw - 150
    print (handPosX, handPosY, handPosZ, grab, hand_pitch)
    wrist_oldf = (map(hand_pitch, 0.3, -0.3, 10, 170))
    hand = (map(grab, 1, 0, 10, 90))
    lenP = 100
    lenQ = 100
    lenR = numpy.sqrt(handPosX**2 + handPosZ**2)
    print("lenR", lenR)
    lenB = numpy.sqrt(lenR**2 + handPosY**2)
    print("lenB", lenB)
    if lenB >= lenP + lenQ or handPosY < 0:
        print("out of range \a")
        return 0
    angH = math.degrees(math.atan(handPosY / lenR))
    print("angH", angH)
    angA = math.degrees(
        math.acos((lenP**2 + lenB**2 - lenQ**2) / (2 * lenP * lenB)))
    print("angA", angA)
    angB = math.degrees(
        math.acos((lenP**2 + lenQ**2 - lenB**2) / (2 * lenP * lenQ)))
    print("angB", angB)
    base = math.degrees(math.atan(-1 * (handPosZ) / handPosX))
    if base < 0:
        base = 180 + base
    print("")
    print("base", base)
    elbow = angA + angH
    print("elbow", elbow)
    arm = angB
    print("arm", arm)
    wrist = (180 - angA + angH)
    print("wrist", wrist)
    print(hand, wrist, arm, elbow, base)
    # serSmooth(hand, wrist, arm, elbow, base)


class SampleListener(Leap.Listener):
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
        if len(frame.hands) == 1:
            hand = frame.hands[0]
            # print("Frame id: %d, timestamp: %d, hands: %d, fingers: %d" % (
            #     frame.id, frame.timestamp, len(frame.hands), len(frame.fingers)))
            # print("  %s, id %d \n  Position: %s" % (
            #     handType, hand.id, hand.palm_position))
            normal = hand.palm_normal
            direction = hand.direction
            # print("    Grab Strength: %s" % (hand.grab_strength))
            # print("    Confidence: %s" % (hand.confidence))
            # print("  Hand:\n    pitch: %f  \n    roll:  %f  \n    yaw:   %f " % (
            #     direction.pitch,
            #     normal.roll,
            #     direction.yaw))
            # print("  hand position: %s" % (
            #     hand.palm_position))
            # print(hand.palm_position[0], hand.palm_position[1],
            #       hand.palm_position[2], hand.grab_strength)
            # print("")
            LeapRaw(hand.palm_position[0], hand.palm_position[1],
                    hand.palm_position[2], hand.grab_strength, direction.pitch)


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


def manu():
    with open('pos.csv', 'rb') as f:
        reader = csv.reader(f)
        pos_list = list(reader)
    sendPos(90, 90, 90, 90, 90)
    # hand,  wrist   arm     elbow   base ; duration, wait
    sleep(1)
    l0, l1, l2, l3, l4 = 90, 90, 90, 90, 90
    for i in pos_list:
        if len(i)!=7:
            break
        steps = float(i[5]) * 100
        p0, p1, p2, p3, p4 = float(i[0]), float(
            i[1]), float(i[2]), float(i[3]), float(i[4])
        s0, s1, s2, s3, s4 = (p0-l0) / steps, (p1-l1) / steps, (p2-l2) / steps, (p3-l3) / steps, (p4-l4) / steps
        # s0, s1, s2, s3, s4 = (l0-p0) / steps, (l1-p1) / steps, (l2-p2) / steps, (l3-p3) / steps, (l4-p4) / steps
        print(i, "   |   " , p0, p1, p2, p3, p4, "   |   ", s0, s1, s2, s3, s4 , "   |   ", l0, l1, l2, l3, l4, "   |   ", steps)
        
        for n in range(int(steps)+1):
            # print "\r %.2f, %.2f, %.2f, %.2f, %.2f" % (p0, p1, p2, p3, p4)
            sendPos(p0, p1, p2, p3, p4)
            sys.stdout.write("\r %.2f, %.2f, %.2f, %.2f, %.2f" %
                                (l0, l1, l2, l3, l4))
            sys.stdout.flush()
            # p0, p1, p2, p3, p4 = p0 + s0, p1 + s1, p2 + s2, p3 + s3, p4 + s4
            l0, l1, l2, l3, l4 = l0 + s0, l1 + s1, l2 + s2, l3 + s3, l4 + s4
            time.sleep(0.01)
        print("")
        # print"" i[5]
        l0, l1, l2, l3, l4 = p0, p1, p2, p3, p4
        time.sleep(float(i[6]))
    print ""

########################################


def control():
    while True:
        try:
            cmd = raw_input("command: ")
            if cmd == 'e':
                break
            elif cmd == 's':
                leapM()
            elif cmd == 'm':
                manu()
            else:
                None
        except:
            print ""
            print "something went wrong... exit? (e)"


if __name__ == "__main__":
    control()
    if connected == True:
        ser.close
