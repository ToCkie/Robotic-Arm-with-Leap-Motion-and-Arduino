# from __future__ import print_function
from time import sleep
import serial
import Leap
import sys
import thread
import time

connected = False
serport = 'COM3'
#serport = '/dev/tty.usbserial'

# while True:
#     sleep(1)
#     try:
#         ser = serial.Serial(serport, 250000)
#         print('Connecting')
#         break
#     except:
#         print "Please connect to port %s (serport)" % (serport)

# while not connected:
#     serin = ser.read()
#     print("Connected")
#     connected = True
#     # print ser.readline()

# ser.write("1")

# while True:
#     print ser.readline()

##################################


def serOutput(hand, wrist, arm, elbow, base):
    if connected = True:
        #!!!!!!!!!!!! ---- THIS LINE NEED TO BE TESTED!!!!
        ser.write(struct.pack('>BBBBB',int(hand), int(wrist), int(arm), int(elbow), int(base))
    return 0
#


def map(var, inL, inH, outL, outH):
    temp = (var - inL) / ((inH - inL) / ((outH - outL) * 1.0))
    if temp > outH:
        return outH
    elif temp < outL:
        return outL
    else:
        return temp


def LeapRaw(a, b, c, d, e, f, g, h, i, j):
    strength, confidence, hand_pitch, hand_yaw, arm_pitch, arm_yaw = a, b, c, d, f, g
    wrist, arm, elbow, base, hand = (map(hand_pitch, -0.7, 0.7, 0, 180)), (map(arm_pitch, -0.3, 0.4, 0, 180)), (map(
        arm_pitch, -0.3, 0.4, 45, 135)), (map(arm_yaw, -0.4, 0.4, 0, 180)), (map(strength, 0, 1, 0, 180))
    print "    hand_pitch: %f \n    arm_pitch:  %f \n    arm_pitch2: %f \n    arm_yaw:    %f \n    strength:   %f" % (
        wrist, arm, elbow, base, hand)

    serOutput(hand, wrist, arm, elbow, base)
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
        if 1 == len(frame.hands):
            # print(frame)
            hand = frame.hands[0]
            normal = hand.palm_normal
            direction = hand.direction
            arm = hand.arm
            LeapRaw(hand.grab_strength, hand.confidence, direction.pitch, direction.yaw, normal.roll,
                    arm.direction[1], arm.direction[0], hand.palm_position, arm.wrist_position, arm.elbow_position)


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
        elif cmd == 'd':
            map(-0, -2, 2, 0, 180)
        elif cmd == 'a':
            None
        else:
            break


if __name__ == "__main__":
    control()
#   ser.close
