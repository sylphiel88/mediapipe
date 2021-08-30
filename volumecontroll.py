import cv2
import time
import handtrackingmodule as htm
import numpy as np
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
vr = volume.GetVolumeRange()
minVol=vr[0]
maxVol=vr[1]


pTime = 0
cTime = 0
cap = cv2.VideoCapture(0)
detector=htm.handDetector(detectionCon=0.8)

while True:
    sucess, img = cap.read()
    img = detector.findHands(img)
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    lmList = detector.findPosition(img)
    if len(lmList)!=0:
        x1,y1 = lmList[4][1],lmList[4][2]
        x2,y2 = lmList[8][1],lmList[8][2]
        cx,cy = (x2+x1)//2,(y1+y2)//2
        cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
        cv2.circle(img,(x2,y2),15,(255,0,255),cv2.FILLED)
        cv2.circle(img,(cx,cy),15,(255,0,255),cv2.FILLED)
        cv2.line(img, (x1,y1),(x2,y2),(255,0,255),2)
        length = math.hypot(x2-x1,y2-y1)
        if length<40:
            length=40
            cv2.circle(img,(cx,cy),15,(0,255,0),cv2.FILLED)
        if length>250:
            length=250
        vol = np.interp(length,[40,250],[minVol, maxVol])
        print(int(length),vol)
        volume.SetMasterVolumeLevel(vol, None)
    cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)