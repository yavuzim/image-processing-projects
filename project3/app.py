import cv2 as cv
import mediapipe as mp
import time 

mpPose = mp.solutions.pose
pose = mpPose.Pose()

mpDraw = mp.solutions.drawing_utils

cap = cv.VideoCapture("video2.mp4")

pTime = 0

while cap.isOpened():
    success, img = cap.read()
    imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    results = pose.process(imgRGB)    
    print(results.pose_landmarks)
    
    if results.pose_landmarks:
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, _ = img.shape
            cx, cy = int(lm.x*w), int(lm.y*h)
            if id == 13:
                cv.circle(img, (cx,cy), 5, (255,0,0), cv.FILLED)
    
    cTime = time.time()
    fps = 1/ (cTime - pTime)
    pTime = cTime
    cv.putText(img, "FPS : "+str(int(fps)), (10,65), cv.FONT_HERSHEY_PLAIN, 2, (255,0,0), 2)
    cv.imshow("img",img)
    if cv.waitKey(25) == ord("q"):
        break
cap.release()
cv.destroyAllWindows()  