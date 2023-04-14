import cv2 as cv
import pickle

width = 27
height = 15

try:
    with open("CarParkPos", "rb") as f: # CarParkPos dosyasına kaydedilen verileri posListe atadık.
        posList = pickle.load(f)
except:
    posList = []
def mouseClick(events, x, y, flags, params):
    if events == cv.EVENT_LBUTTONDOWN: # sol tık yapılırsa ilgili konum posList dizisine eklenecek.
        posList.append((x, y))
    if events == cv.EVENT_RBUTTONDOWN: # sağ tık yapılırsa ilgili konum posListten silinecek.
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                posList.pop(i)
    with open("CarParkPos", "wb") as f: # posList dizisi CarParkPos dosyasına kaydedildi.
        pickle.dump(posList, f)

while True:
    img = cv.imread("first_frame.png") # resmi içeri aktardık.  
    for pos in posList:
        cv.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 0), 2) # posList dizisinin içindeki konumlara göre kare çizdik.
    cv.imshow("img",img) # resmi ekranda gösterdik.
    cv.setMouseCallback("img", mouseClick) # mouse tıklandığında gerçekleşek olay. mouseClick metoduna gider.
    if cv.waitKey(1) == ord("q"):
        break 
    
cv.destroyAllWindows()