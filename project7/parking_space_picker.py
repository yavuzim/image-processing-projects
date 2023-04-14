import cv2 as cv
import pickle

width = 27
height = 15

try:
    with open("CarParkPos", "rb") as f:
        posList = pickle.load(f)
except:
    posList = []
def mouseClick(events, x, y, flags, params):
    if events == cv.EVENT_LBUTTONDOWN:
        posList.append((x,y))
    if events == cv.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x <x1 + width and y1 < y < y1 + height:
                posList.pop(i)
    with open("CarParkPos", "wb") as f:
        pickle.dump(posList, f)

while True:
    img = cv.imread("first_frame.png")   
    for pos in posList:
        cv.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255,0,0), 2)
     
    cv.imshow("img",img)
    cv.setMouseCallback("img", mouseClick)
    if cv.waitKey(1) == ord("q"):
        break
    




cv.destroyAllWindows()