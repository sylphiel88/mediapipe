import handtrackingmodule as htm
import numpy as np
import cv2
import time

cap = cv2.VideoCapture(0)
pTime = 0
cTime = 0
cap = cv2.VideoCapture(0)
detector = htm.handDetector(detectionCon=0.5)

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    lmList = detector.findPosition(img)
    detector.getFingers(lmList)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
