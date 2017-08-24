# from __future__ import print_function
from time import sleep
import serial
import Leap, sys, thread, time

serport = 'COM3'
#serport = '/dev/tty.usbserial'

while True:
    sleep(1)
    try:
        ser = serial.Serial(serport, 250000)
        print('Connecting')
        break
    except: 
        print "Please connect to port %s (serport)" %(serport)
        
connected = False

while not connected:
    serin = ser.read()
    print("Connected")
    connected = True
    # print ser.readline()

# ser.write("1")

# while True:
#     print ser.readline()

##################################
def serOutput(wrist, arm, elbow, base, hand):
    return 0
#
def map(var, inL, inH, outL, outH):
    #print(var, inL, inH, outL, outH)
    temp = (var-inL) / ((inH - inL)/((outH - outL) * 1.0))
    #print(temp)
    if temp > outH:     return outH
    elif temp < outL:   return outL
    else:               return temp
#

def LeapRaw(a,b,c,d,e,f,g,h,i,j):
    #print(a,b,c,d,e,f,g,h,i,j)
    """
        a == hand.grab_strength, 
        b == hand.confidence, 
        c == direction.pitch, 
        d == direction.yaw, 
        e == normal.roll, 
        f == arm.direction[1],
        g == arm.direction[0], 
        h == hand.palm_position, 
        i == arm.wrist_position, 
        j == arm.elbow_position)
    """
    strength,confidence,hand_pitch,hand_yaw,arm_pitch,arm_yaw = a,b,c,d,f,g
    # print "  strength:   %s \n  confidence: %s \n  hand_pitch: %s \n  hand_yaw:   %s \n  arm_pitch:  %s \n  arm_yaw:    %s \n ---------------------------" % ( strength, confidence, hand_pitch, hand_yaw, arm_pitch, arm_yaw)
    #

    wrist, arm, elbow, base, hand = (map(hand_pitch, -0.7, 0.7, 0, 180)), (map(arm_pitch, -0.3, 0.4, 0, 180)), (map(arm_pitch, -0.3, 0.4, 45, 135)), (map(arm_yaw, -0.4, 0.4, 0, 180)), (map(strength, 0, 1, 0, 180))
    print "    hand_pitch: %f \n    arm_pitch:  %f \n    arm_pitch2: %f \n    arm_yaw:    %f \n    strength:   %f" %(
        (map(hand_pitch, -0.7, 0.7, 0, 180)), (map(arm_pitch, -0.3, 0.4, 0, 180)), (map(arm_pitch, -0.3, 0.4, 45, 135)), (map(arm_yaw, -0.4, 0.4, 0, 180)), (map(strength, 0, 1, 0, 180)))
    serOutput(wrist, arm, elbow, base, hand)
    print('----------------------------------')

    ser.write(int((map(hand_pitch, 0, 1, 0, 180))))
    # serialRead = ser.readline()
    # print(serialRead)
    print ser.readline()
    ##


#
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
        # print("Frame id: %d, timestamp: %d, hands: %d, fingers: %d" % (
        #       frame.id, frame.timestamp, len(frame.hands), len(frame.fingers)))
        for hand in frame.hands:
            print(frame)
            handType = "Left hand" if hand.is_left else "Right hand"
            # print("  %s, id %d \n  Position: %s" % (
            #     handType, hand.id, hand.palm_position))
            normal = hand.palm_normal
            direction = hand.direction
            # print("    Grab Strength: %s" %(hand.grab_strength))
            # print("    Confidence: %s" %(hand.confidence))
            # print("  Hand:\n    pitch: %f  \n    roll:  %f  \n    yaw:   %f " % (
            #     direction.pitch,
            #     normal.roll,
            #     direction.yaw))
            arm = hand.arm
            # print("  Arm direction: \n    pitch: %f  \n    yaw:   %f " % (
            #     arm.direction[1],
            #     arm.direction[0]))s
            # print("  wrist position: %s \n  elbow position: %s" % (
            #     arm.wrist_position,
            #     arm.elbow_position))   
            # print("")
            # print(hand.grab_strength, hand.confidence,direction.pitch,direction.yaw,arm.direction[1],arm.direction[0])
            LeapRaw(hand.grab_strength, hand.confidence, direction.pitch, direction.yaw, normal.roll, arm.direction[1],arm.direction[0], hand.palm_position, arm.wrist_position, arm.elbow_position)

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
        if cmd == 'e':      break
        elif cmd == 's':    leapM()
        elif cmd == 'd':    map(-0,-2,2,0,180)
        elif cmd == 'a':    
            None
        else: break


if __name__ == "__main__":
    control()
#   ser.close