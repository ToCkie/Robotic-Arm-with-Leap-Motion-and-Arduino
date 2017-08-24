import Leap, sys, thread, time

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
        print("Frame id: %d, timestamp: %d, hands: %d, fingers: %d" % (
              frame.id, frame.timestamp, len(frame.hands), len(frame.fingers)))
        for hand in frame.hands:
            handType = "Left hand" if hand.is_left else "Right hand"
            print("  %s, id %d \n  Position: %s" % (
                handType, hand.id, hand.palm_position))
            normal = hand.palm_normal
            direction = hand.direction
            print("    Grab Strength: %s" %(hand.grab_strength))
            print("    Confidence: %s" %(hand.confidence))
            print("  Hand:\n    pitch: %f  \n    roll:  %f  \n    yaw:   %f " % (
                direction.pitch,
                normal.roll,
                direction.yaw))
            arm = hand.arm
            print("  Arm direction: \n    pitch: %f  \n    yaw:   %f \n    ?????: %f" % (
                arm.direction[1],
                arm.direction[0],
                arm.direction[2]))
            print("  wrist position: %s \n  elbow position: %s" % (
                arm.wrist_position,
                arm.elbow_position))   
            print("")

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


if __name__ == "__main__":
    leapM()
