# -*- coding: utf-8 -*-
import os
import cv2


os.mkdir("./collect/")
cap = cv2.VideoCapture(0)
i = 0
while True:
    ret, frame = cap.read()
    if ret:
        cv2.imshow("capture", frame)
    k = cv2.waitKey(1)
    if k == ord(' '):
        break
    elif k == ord('s'):
        cv2.imwrite(f"./collect/{i}.jpg", frame)
        i = i + 1
cap.release()
cv2.destroyAllWindows()
