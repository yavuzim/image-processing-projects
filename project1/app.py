import cv2 as cv
import time
import mediapipe as mp

cap = cv.VideoCapture(0)

mpHand = mp.solutions.hands
hands = mpHand.Hands()
mpDraw = mp.solutions.drawing_utils

while cap.isOpened() | cv.waitKey(1)!=ord("q"):
    success, img = cap.read() 
    imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    print(results.multi_hand_landmarks)
    
    if results.multi_hand_landmarks: # None değilse sağlayacak.
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLms, mpHand.HAND_CONNECTIONS)
    
    cv.imshow("img",img)
   

cap.release()
cv.destroyAllWindows()