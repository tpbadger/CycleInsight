import serial
import time
ser = serial.Serial('/dev/ttyUSB0', baudrate = 115200, timeout = 2)
data = "go"
data += "\r\n"
time.sleep(2)
ser.write(data.encode())

while 1:
    print(ser.readline())
