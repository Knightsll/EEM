import cv2
import time

cap = cv2.VideoCapture(0)
time.sleep(2)
ok, img = cap.read()
print ok
cv2.imwrite(r'./wechat.jpg',img)
