import cv2
import numpy as np
import time
import os
import numpy as np


face_cascade = cv2.CascadeClassifier(r'/home/pi/opencv-3.4.1/data/haarcascades/haarcascade_frontalface_default.xml')
#if you just have one camera it should be 0. if else, please seach for the camera which you want to use and change the port
cap=cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_SIMPLEX
t = 0
a = 1
while True:
    ok, img = cap.read()
    if t == 40:
        gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.35,
            minNeighbors=5,
            minSize=(6, 6),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        t = 0
    else:
        t+=2
    try:
        for(x, y, w, h) in faces:
            cv2.circle(img, (np.int(((x+x+w)/2)), np.int((y+y+h)/2)), np.int(w/2), (255, 255, 255), 3)
            cv2.putText(img, 'HEY I FOUND YOU', (np.int(((x+x+w)/2)), np.int((y+y+h)/2+20)),font,1.2,(0,255,255),2)
        cv2.imshow("Face",img)
        if len(faces)!=0:
            if a == 1 :
                os.system('python ~/Desktop/EEM/baidu_STT/EEm.py')
                a-=1
                time.sleep(1)
        else:
            pass
    except:
        cv2.imshow("Face",img)
        
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
