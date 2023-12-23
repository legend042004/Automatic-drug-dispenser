import serial

s1 = serial.Serial('COM7',9600,timeout=1)

while 1:
    ser = s1.readline().decode()
    print(ser) 