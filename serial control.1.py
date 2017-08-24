# from __future__ import print_function
from time import sleep
import serial
import Leap
import sys
import thread
import time
import struct
import csv

connected = False
# serport = 'COM3'
serport = '/dev/cu.wchusbserial1440'

while True:
    sleep(1)
    try:
        ser = serial.Serial(serport, 250000)
        print('Connecting')
        break
    except:
        print "Please connect to port %s (serport)" % (serport)

while not connected:
    serin = ser.read()
    print("Connected")
    connected = True
    # print ser.readline()

# ser.write("1")

# while True:
#     print ser.readline()

##################################


def serOutput(hand, wrist, arm, elbow, base):
    if connected == True:
        #!!!!!!!!!!!! ---- THIS LINE NEED TO BE TESTED!!!!
        ser.write(struct.pack('>BBBBB', int(hand), int(wrist), int(arm), int(elbow), int(base)))
    return 0


def map(var, inL, inH, outL, outH):
    temp=(var - inL) / ((inH - inL) / ((outH - outL) * 1.0))
    if temp > outH:
        return outH
    elif temp < outL:
        return outL
    else:
        return temp


########################################

def test1():
    with open('pos.csv', 'rb') as f:
        reader = csv.reader(f)
        pos_list = list(reader)
    #serOutput(hand, wrist, arm, elbow, base)
    serOutput(90,90,90,90,90)
        #hand,  wrist   arm     elbow   base
    pos = [

        ]
    sleep(1)

    for i in pos_list:
        print(i)
        try:
            serOutput(int(i[0]),int(i[1]),int(i[2]),int(i[3]),int(i[4]))
            sleep(float(i[5]))
        except:
            pass


def control():
    while True:
        cmd=raw_input("command: ")
        if cmd == 't':
            test1()
        elif cmd == 'a':
            None
        else:
            None


if __name__ == "__main__":
    control()
#   ser.close
