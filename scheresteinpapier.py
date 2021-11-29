import cv2
import handtrackingmodule as htm
import random
import numpy as np

onebool, twobool, threebool, wahlbool, choosebool, winbool, play = True, True, True, True, False, False, True
wahl = ""
wahlp = ""
wintext = ""
punktep = 0
punktec = 0

cap = cv2.VideoCapture(0)
detector = htm.handDetector(detectionCon=0.8)
pTime = 0
cTime = 0
i = 0
j = -1


def exitgame(event, x, y, flags, param):
    global play
    if event == cv2.EVENT_LBUTTONDOWN:
        if 1240 < x <= 1280:
            if 0 < y <= 100:
                play = False


img = np.zeros((512, 512, 3), np.uint8)
cv2.namedWindow('Schere, Stein, Papier')
cv2.setMouseCallback('Schere, Stein, Papier', exitgame)

while play:
    sucess, img = cap.read()
    img = detector.findHands(img, draw=False)
    # cTime = time.time()
    # fps = 1 / (cTime - pTime)
    # pTime = cTime
    # cv2.putText(img, str(int(fps)), (40, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 5)
    positions = detector.findPosition(img, draw=False)
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
        cv2.putText(img, "Schere,", (40, 120), cv2.FONT_HERSHEY_PLAIN, 2, (180, 180, 180), 10)
        cv2.putText(img, "Schere,", (40, 120), cv2.FONT_HERSHEY_PLAIN, 2, (60, 60, 60), 5)
    if not twobool:
        cv2.putText(img, "Stein,", (170, 120), cv2.FONT_HERSHEY_PLAIN, 2, (180, 180, 180), 10)
        cv2.putText(img, "Stein,", (170, 120), cv2.FONT_HERSHEY_PLAIN, 2, (60, 60, 60), 5)
    if not threebool:
        choosebool = False
        j += 1
        cv2.putText(img, "Papier. Go!", (270, 120), cv2.FONT_HERSHEY_PLAIN, 2, (180, 180, 180), 10)
        cv2.putText(img, "Papier. Go!", (270, 120), cv2.FONT_HERSHEY_PLAIN, 2, (60, 60, 60), 5)
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
    # cv2.putText(img, str(fingers), (40, 80), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 5)
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
            punktep += 1
        elif (wahl == "Papier" and wahlp == "Schere") or (wahl == "Schere" and wahlp == "Stein") or (
                wahl == "Stein" and wahlp == "Papier"):
            wintext = "Verloren!"
            punktec += 1
            winbool = True
    computer = np.zeros((480, 640, 3), np.uint8)
    if winbool:
        cv2.putText(img, wahl, (40, 160), cv2.FONT_HERSHEY_PLAIN, 2, (0, 60, 0), 10)
        cv2.putText(img, wahl, (40, 160), cv2.FONT_HERSHEY_PLAIN, 2, (0, 180, 0), 5)
        cv2.putText(img, wahlp, (200, 160), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 60), 10)
        cv2.putText(img, wahlp, (200, 160), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 180), 5)
        cv2.putText(img, wintext, (40, 200), cv2.FONT_HERSHEY_PLAIN, 2, (60, 60, 60), 10)
        cv2.putText(img, wintext, (40, 200), cv2.FONT_HERSHEY_PLAIN, 2, (180, 180, 180), 5)
        wahlpcp = cv2.imread(wahlp + ".png")
        wahlpp = cv2.imread(wahl + ".png")
        computer = cv2.addWeighted(computer, 0, wahlpcp, 1, 0)
        img = cv2.addWeighted(img, 0.8, wahlpp, 0.2, 0)
        if fingers == 1:
            # noinspection PyRedeclaration
            onebool, choosebool, twobool, threebool, wahlbool, choosebool = True, True, True, True, True, False
            i, wahl, wahlp, winbool, j = 0, "", "", False, -1
    cv2.putText(img, "P", (500, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 60, 0), 10)
    cv2.putText(img, "P", (500, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 180, 0), 5)
    cv2.putText(img, "|", (535, 40), cv2.FONT_HERSHEY_PLAIN, 2, (180, 180, 180), 10)
    cv2.putText(img, "|", (535, 40), cv2.FONT_HERSHEY_PLAIN, 2, (60, 60, 60), 5)
    cv2.putText(img, "C", (560, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 60), 10)
    cv2.putText(img, "C", (560, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 180), 5)
    cv2.putText(img, str(punktep), (500, 80), cv2.FONT_HERSHEY_PLAIN, 2, (0, 60, 0), 10)
    cv2.putText(img, str(punktep), (500, 80), cv2.FONT_HERSHEY_PLAIN, 2, (0, 180, 0), 5)
    cv2.putText(img, "|", (535, 80), cv2.FONT_HERSHEY_PLAIN, 2, (180, 180, 180), 10)
    cv2.putText(img, "|", (535, 80), cv2.FONT_HERSHEY_PLAIN, 2, (60, 60, 60), 5)
    cv2.putText(img, str(punktec), (560, 80), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 60), 10)
    cv2.putText(img, str(punktec), (560, 80), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 180), 5)
    cv2.putText(computer, "X", (600, 25), cv2.FONT_HERSHEY_PLAIN, 2, (60, 60, 60), 10)
    cv2.putText(computer, "X", (600, 25), cv2.FONT_HERSHEY_PLAIN, 2, (180, 180, 180), 5)
    bild = np.concatenate((img, computer), axis=1)
    cv2.imshow("Schere, Stein, Papier", bild)
    cv2.waitKey(1)

cv2.destroyAllWindows()