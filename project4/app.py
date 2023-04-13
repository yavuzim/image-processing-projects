import cv2 as cv
import numpy as np
import mediapipe as mp
import math 

def findAngle(img, p1, p2, p3, lmList, draw = True):
    x1, y1 = lmList[p1][1:] 
    x2, y2 = lmList[p2][1:] 
    x3, y3 = lmList[p3][1:] 
    
    # açı hesaplama
    angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
    if angle < 0:
        angle += 360
    if draw:
        cv.line(img, (x1, y1), (x2, y2), (0,0,255), 3)
        cv.line(img, (x3, y3), (x2, y2), (0,0,255), 3)
        
        cv.circle(img, (x1, y1), 10, (0,255,255), cv.FILLED)
        cv.circle(img, (x2, y2), 10, (0,255,255), cv.FILLED)
        cv.circle(img, (x3, y3), 10, (0,255,255), cv.FILLED)
        
        cv.circle(img, (x1, y1), 15, (0,255,255))
        cv.circle(img, (x2, y2), 15, (0,255,255))
        cv.circle(img, (x3, y3), 15, (0,255,255))
        
        cv.putText(img, str(int(angle)), (x2 - 40, y2 - 40), cv.FONT_HERSHEY_PLAIN, 2, (0,255,255), 2)
    return angle

cap = cv.VideoCapture("video1.mp4")

mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils
dir = 0
count = 0
while cap.isOpened():
    success, img = cap.read()
    imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    results = pose.process(imgRGB)
    lmList = []
    if results.pose_landmarks:
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, _ = img.shape
            cx, cy = int(lm.x*w), int(lm.y*h)
            lmList.append([id, cx, cy])
    if len(lmList) != 0:
        # şınav
        angle = findAngle(img, 11, 13, 15, lmList)
        per = np.interp(angle, (185, 245), (0, 100)) # 185 245 arası bir tekrar için. 0 100 arasına sıkıştırdık.
        if per == 100:
            if dir == 0:
                count += 0.5
                dir = 1
        if per == 0:
            if dir == 1:
                count += 0.5
                dir = 0
        cv.putText(img, "Sinav Sayisi : "+str(int(count)), (45, 125), cv.FONT_HERSHEY_PLAIN, 2, (255,0,0), 8)                      
        
    cv.imshow("img",img)
    if cv.waitKey(10) == ord("q"):
        break

cap.release()
cv.destroyAllWindows()
    