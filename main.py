from pyfirmata import Arduino, SERVO, util
from time import sleep
import serial
import cv2
import threading 
import mysql.connector

cap=cv2.VideoCapture(0)
detector=cv2.QRCodeDetector()
s1 = serial.Serial('COM7',9600,timeout=1)
port = 'COM9'
pin1 = 5
pin2 = 4
pin3 = 3
board = Arduino(port)
connection = mysql.connector.connect(host ="localhost", user = "root" , password = "", database = "maindb")
mycursor = connection.cursor()
 
if board:
    print("Successfully connected to Arduino")

board.digital[pin1].mode = SERVO
board.digital[pin2].mode = SERVO
board.digital[pin3].mode = SERVO    

def serialread():
    while True:
        ser = s1.readline().decode()
        print(ser)
        sleep(1)
           
def select(id):
    if id=="1":
        rotateservo(pin1)
        sql = "UPDATE medicine SET medicineQuantity = medicineQuantity-1 WHERE medicineId = 1"
        mycursor.execute(sql)
        connection.commit()
        
    elif id=="2":
        rotateservo1(pin2)  
        sql = "UPDATE medicine SET medicineQuantity = medicineQuantity-1 WHERE medicineId = 2"
        mycursor.execute(sql)
        connection.commit()

    elif id=="3":
        rotateservo1(pin3)  
        sql = "UPDATE medicine SET medicineQuantity = medicineQuantity-1 WHERE medicineId = 3"
        mycursor.execute(sql)
        connection.commit()
    else :
        print("abc")

def rotateservo(pin):
    board.digital[pin].write(180)  
    sleep(2.5)
    board.digital[pin].write(90)   
    sleep(1)

def rotateservo1(pin):
    board.digital[pin].write(0)  
    sleep(2.5)
    board.digital[pin].write(90)   
    sleep(1)

def webcam():
    while True:
       
        _,img=cap.read()
        data,one, _=detector.detectAndDecode(img)
        if data:
            print("the data in qr is")
            print(data)
            lines = data.splitlines()
            for line in lines:
                x = line.split()
                if len(x) >= 2:  
                    id = x[0]
                    qty = x[1]
                    select(id)
                else:
                    print(f"Invalid data: {line}")
                
            break
        cv2.imshow('qrscanner app',img)
        if cv2.waitKey(1)==ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
   
board.digital[pin1].write(90)
board.digital[pin2].write(90)
board.digital[pin3].write(90)
    


thread1 = threading.Thread(target=serialread)
thread2 = threading.Thread(target=webcam)

thread1.start()
thread2.start()

thread1.join()
thread2.join()

    
board.exit()  
