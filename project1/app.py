import cv2 as cv
import time
import mediapipe as mp

cap = cv.VideoCapture(0)

mpHand = mp.solutions.hands
hands = mpHand.Hands()
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

while cap.isOpened() | cv.waitKey(1)!=ord("q"):
    success, img = cap.read() 
    imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    print(results.multi_hand_landmarks)
    
    if results.multi_hand_landmarks: # None değilse sağlayacak.
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLms, mpHand.HAND_CONNECTIONS)
            for id, lm in enumerate(handLms.landmark):
                #print(id,lm)
                h, w, c = img.shape 
                cx, cy = int(lm.x*w), int(lm.y*h)                
                
                if id == 0: # bilek
                    cv.circle(img, (cx,cy), 9, (255,0,0), cv.FILLED)
                if id == 20: # serçe parmağın en uç noktası
                    cv.circle(img, (cx,cy), 9, (255,0,0), cv.FILLED)                    
                
    # fps hesaplama
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    
    cv.putText(img, "FPS : "+str(int(fps)), (10,75), cv.FONT_HERSHEY_PLAIN, 3, (255,0,0), 5)
    
    cv.imshow("img",img)
   

cap.release()
cv.destroyAllWindows()