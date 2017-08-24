from time import sleep
import serial
import Leap, sys, thread, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

serport = '/dev/tty.usbserial'

while True:
    sleep(1)
    try:
        ser = serial.Serial(serport, 9600)
        break
    except: 
        print "Please connect to port %s (serport)" %(serport)
        
connected = False
while not connected:
    serin = ser.read()
    print("Connected")
    connected = True


ser.write("1")



ser.close

def control():
    while true:
        command = input("command: ")

if __name__ == "__main__":
    control()
