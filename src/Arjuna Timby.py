import cv2  #openCV
from cvzone.HandTrackingModule import HandDetector #hand tracking
import numpy as np  #Z axis calculation
import cvzone  #handtracking
import Angles  #turret angles
import serial  #usb communication

# webcam
camera = cv2.VideoCapture(0)  #turn on webcam
camera.set(3, 1280)           #window width
camera.set(4,720)             #window height

# USB
serialcomm = serial.Serial('COM3', 9600)
serialcomm.timeout = 1

# Hand detector
detector = HandDetector(detectionCon=0.8, maxHands=1)

# find function
x = [193, 153, 129, 107, 97, 86, 78, 70, 64, 59, 56, 50, 49, 46, 43, 40,  38, ]
y = [20,   25,  30,  35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, ]
coff = np.polyfit(x,y,2)   # y = Ax2 + Bx + C
A, B, C = coff
#print(A, B, C)
A = 0.012636680507237852
B = -2.710541724316941
C = 182.62076069382988

while True:
    success, img = camera.read()
    hands = detector.findHands(img, draw=False)

    if hands:
        lmList = hands[0]['lmList']
        bx, by, bw, bh = hands[0]['bbox']
        hand_x1, hand_y1 = lmList[5]
        hand_x2, hand_y2 = lmList[17]
        center_x = abs((hand_x2+hand_x1)/2)
        center_y = abs((hand_y2+hand_y1)/2)

        distance_virtual = (((hand_x2-hand_x1)**2) + ((hand_y2 - hand_y1)**2))**(1/2)  #dist b/w pt 5 & 17

        # Z axis calculation
        if distance_virtual > 153 :
            Z_real = (-0.125*distance_virtual)+44.125

        elif distance_virtual < 153 and distance_virtual > 107:
            Z_real = (-0.217391304348*distance_virtual) + 58.2608695652

        else:
            Z_real = (A * (distance_virtual**2)) + (B * distance_virtual) + C

        # X, Y axis calculation
        scrnCenter_x = 512
        scrnCenter_y = 288
        X_virtual = -(center_x - scrnCenter_x)
        Y_virtual = -(center_y - scrnCenter_y)
        X_real = X_virtual * (6.3/distance_virtual)
        Y_real = Y_virtual * (6.3/distance_virtual)


        cvzone.putTextRect(img,f'{int(X_real)}cm {int(Y_real)}cm {int(Z_real)}cm', (bx, by))
        cv2.circle(img, (512,288), 2, (0,0,255), 2)
        cv2.rectangle(img, (bx-5,by-5), (bx+bw+2, by+bh+2), (255,0,0), 2, 5)

        angles = Angles.turret(X_real, Y_real, Z_real)
        angles.offsets(12, 0, 7)
        angles.getAngles()

        # Z_real = A*(distance_virtual**2) + B*(distance_virtual) + C
        # print("d:", int(distance_virtual))
        # print("Z:", int(Z_real))
        #print("X:", int(X_real))
        #print("Y:", int(Y_real))
        #print(int(angles.getTheta_x()))
        #print(int(angles.getTheta_y()))

        motorX = "%" + "X" + str(int(angles.getTheta_x())+10) + "#"
        motorY = "%" + "Y" + str(int(angles.getTheta_y())+3) + "#"
        #print("MY", motorY)
        serialcomm.write(motorX.encode())
        #time.sleep(0.5)
        serialcomm.write(motorY.encode())
        #print(serialcomm.readline())

    cv2.imshow("win name", img)
    cv2.waitKey(1)
