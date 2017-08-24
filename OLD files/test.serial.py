# from __future__ import print_function
from time import sleep
import serial
import struct
import Leap, sys, thread, time

serport = 'COM3'
serport = '/dev/tty.usbserial'
serport = '/dev/cu.wchusbserial1440'
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

while True:
    # ser.write(int(input(': ')))
    ser.write(struct.pack('>B',int(input(': '))))
    print ser.readline()