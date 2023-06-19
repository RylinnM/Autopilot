import cv2
from cvzone.HandTrackingModule import HandDetector
import socket

host = "xxxx"
port = 6666
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mySocket.bind((host, port))
mySocket.listen(5)
client, address = mySocket.accept()

cap=cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,720)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
detector=HandDetector(detectionCon=0.8, maxHands=2)
while True:
    if cv2.waitKey(25) & 0xFF == ord('q'): 
        break
    success,img=cap.read()
    img=cv2.flip(img,1)
    lmlist,img=detector.findHands(img)
    cv2.imshow("Image",img)
    cv2.waitKey(1)
    if len(lmlist)<2:
        print("stop")
        client.send("0".encode("utf-8"))
    if len(lmlist)==2:
        if lmlist[0]['type']=='Right':
            lefthand=lmlist[0]
            righthand=lmlist[1]
        else:
            lefthand=lmlist[1]
            righthand=lmlist[0]
        righthand=lmlist[0]['center'][1]
        lefthand=lmlist[1]['center'][1]
        if righthand>lefthand+200:
            print('turn left')
            client.send("1".encode("utf-8"))

        elif righthand+200<lefthand:
            print('turn right')
            client.send("2".encode("utf-8"))
        else:
            print('go straight')
            client.send("3".encode("utf-8"))


cv2.destroyAllWindows()
cap.release()