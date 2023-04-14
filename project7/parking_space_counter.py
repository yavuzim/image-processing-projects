import cv2 as cv
import pickle
import numpy as np

def checkParkSpace(imgg):
    spaceCounter = 0 # Boşlukları tutar.
    for pos in posList:
        x, y = pos
        img_crop = imgg[y: y + height, x: x + width]
        count = cv.countNonZero(img_crop)
        print("count : ",count)
        
        if count < 180: # boşsa
            color = (0, 255, 0)
            thickness = 2
            spaceCounter += 1
        else:
            color = (0, 0, 255)
            thickness = 2
        cv.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness) # posList dizisinin içindeki konumlara göre kare çizdik.
        cv.putText(img, str(count), (x, y + height - 2), cv.FONT_HERSHEY_PLAIN, 1, color, 1)
    cv.putText(img, f"Free :  {spaceCounter}/{len(posList)}", (15, 15), cv.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 2)      

width = 27
height = 15

cap = cv.VideoCapture("video.mp4")

with open("CarParkPos", "rb") as f:
    posList = pickle.load(f)

while cap.isOpened():
    success, img = cap.read()
    imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    imgGauss = cv.GaussianBlur(imgGray, (3, 3), 1)
    imgThreshold = cv.adaptiveThreshold(imgGauss, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv.medianBlur(imgThreshold, 5)
    imgDilate = cv.dilate(imgMedian, np.ones((3, 3)), iterations = 1) # beyazları kalınlaştırdı.
    checkParkSpace(imgDilate)
    cv.imshow("img",img)
    if cv.waitKey(200) == ord("q"):
        break

cap.release()
cv.destroyAllWindows()