import cv2 as cv
import mediapipe as mp

cap = cv.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

mpHand = mp.solutions.hands
hands = mpHand.Hands()

mpDraw = mp.solutions.drawing_utils

tipIds = [4, 8, 12, 16, 20]

while cap.isOpened() | cv.waitKey(1) != ord("q"):
    success, img = cap.read()
    imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)    
    
    results = hands.process(img)
    print(results.multi_hand_landmarks)
    
    lmList = []
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLms, mpHand.HAND_CONNECTIONS)
            
            for id, lm in enumerate(handLms.landmark):
                h, w, _ = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                lmList.append([id, cx, cy])
                    
    if len(lmList) != 0:
        fingers = []
        
        # baş parmak
        if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else: fingers.append(0)
        
        # diğer 4 parmak
        for id in range(1,5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
                
        totalF = fingers.count(1)
        cv.putText(img, "Parmak Sayisi : "+str(totalF), (10,75), cv.FONT_HERSHEY_PLAIN, 3, (255,0,0), 5)
    else:
        cv.putText(img, "Parmaklar Yok", (10,75), cv.FONT_HERSHEY_PLAIN, 3, (255,0,0), 5)   
                
    cv.imshow("Kamera",img)


cap.release()
cv.destroyAllWindows()