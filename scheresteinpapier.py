import cv2
import time
import handtrackingmodule as htm
import numpy as np
import math
import random

onebool, twobool, threebool, wahlbool,choosebool,winbool = True, True, True, True, False,False
wahl = ""
wahlp = ""
cap = cv2.VideoCapture(0)
detector = htm.handDetector(detectionCon=0.8)
pTime = 0
cTime = 0
i = 0
j = -1
while True:
    sucess, img = cap.read()
    img = detector.findHands(img)
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (40, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 5)
    positions = detector.findPosition(img)
    fingers = sum(detector.getFingers(positions))
    if (i == 0 and fingers == 1) and onebool:
        i += 1
        onebool = False
    if (i == 1 and fingers == 2) and twobool:
        i += 1
        twobool = False
    if (i == 2 and fingers == 3) and threebool:
        i += 1
        threebool = False
    if not onebool:
        cv2.putText(img, "Schere,", (40, 120), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 5)
    if not twobool:
        cv2.putText(img, "Stein,", (170, 120), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 5)
    if not threebool:
        choosebool = False
        j += 1
        cv2.putText(img, "Papier. Go!", (270, 120), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 5)
    if j >= 10 and wahlbool:
        if fingers == 0:
            wahl = "Stein"
            wahlbool = False
        elif fingers == 2:
            wahl = "Schere"
            wahlbool = False
        elif fingers == 5:
            wahl = "Papier"
            wahlbool = False
        else:
            wahl = "Choose faster"
            onebool, choosebool, twobool, threebool, j, i = True, True, True, True, -1, 0
    cv2.putText(img, str(fingers), (40, 80), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 5)
    if (not wahlbool or choosebool) and not winbool:
        pc = random.randint(0, 2)
        if pc == 0:
            wahlp = "Schere"
        elif pc == 1:
            wahlp = "Stein"
        else:
            wahlp = "Papier"
        if wahl == wahlp:
            wintext = "Unentschieden"
            winbool = True
        elif (wahl == "Schere" and wahlp == "Papier") or (wahl == "Stein" and wahlp == "Schere") or (
                wahl == "Papier" and wahlp == "Stein"):
            wintext = "Gewonnen!"
            winbool = True
        elif (wahl == "Papier" and wahlp == "Schere") or (wahl == "Schere" and wahlp == "Stein") or (
                wahl == "Stein" and wahlp == "Papier"):
            wintext = "Verloren!"
            winbool = True
    if winbool:
        cv2.putText(img, wahl, (40, 160), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 5)
        cv2.putText(img, wahlp, (40, 200), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 5)
        cv2.putText(img, wintext, (40, 240), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 5)
        if fingers == 1:
            onebool, choosebool, twobool, threebool,wahlbool,choosebool= True, True, True, True, True,False
            i,wahl,wahlp,winbool, j =0,"","",False, -1
    cv2.imshow("SSP", img)
    cv2.waitKey(1)