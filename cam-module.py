
import cv2

cap=cv2.VideoCapture(0)
detector=cv2.QRCodeDetector()

while True:
    _,img=cap.read()
    data,one, _=detector.detectAndDecode(img)
    if data:
        print("the data in qr is")
        print(data)
        break
    cv2.imshow('qrscanner app',img)
    if cv2.waitKey(1)==ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
