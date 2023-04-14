import cv2 as cv
import mediapipe as mp
import time

cap = cv.VideoCapture("video1.mp4")

mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh(max_num_faces = 1)  

mpDraw = mp.solutions.drawing_utils
drawSpec = mpDraw.DrawingSpec(thickness = 1, circle_radius = 1)

pTime = 0

while cap.isOpened():
    success, img = cap.read()
    imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    results = faceMesh.process(imgRGB)
    if results.multi_face_landmarks:
        for faceLms in results.multi_face_landmarks:
            mpDraw.draw_landmarks(img, faceLms, mpFaceMesh.FACEMESH_TESSELATION, drawSpec, drawSpec) # FACEMESH_CONTOURS
            for id, lm in enumerate(faceLms.landmark):
                h, w, _ = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                print([id, cx, cy])
    
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv.putText(img, "FPS : "+str(int(fps)), (10,65), cv.FONT_HERSHEY_PLAIN, 2, (255,0,0), 2)
            
    
    cv.imshow("img",img)    
    if cv.waitKey(10) == ord("q"):
        break
    
cap.release()
cv.destroyAllWindows()