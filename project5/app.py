import cv2 as cv
import mediapipe as mp

cap = cv.VideoCapture("video3.mp4")

mpFaceDetection = mp.solutions.face_detection
faceDetection = mpFaceDetection.FaceDetection()

mpDraw = mp.solutions.drawing_utils 

while cap.isOpened():
    success, img = cap.read()
    imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    results = faceDetection.process(imgRGB)
    if results.detections:
        for id, detection in enumerate(results.detections):
            bboxC = detection.location_data.relative_bounding_box
            h, w, _ = img.shape
            bbox = int(bboxC.xmin*w), int(bboxC.ymin*h), int(bboxC.width*w), int(bboxC.height*h)
            cv.rectangle(img, bbox, (0, 255, 255), 2)
    
    cv.imshow("img",img)    
    if cv.waitKey(10) == ord("q"):
        break
    
cap.release()
cv.destroyAllWindows()