# -*- coding: utf-8 -*-
import os
import cv2


os.makedirs("./collect/cola", exist_ok=True)
os.makedirs("./collect/sprite", exist_ok=True)
os.makedirs("./collect/fanta", exist_ok=True)
os.makedirs("./collect/gum", exist_ok=True)
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
        if 0 <= i < 25:
            cv2.imwrite(f"./collect/cola/{i}.jpg", frame)
        elif 25 <= i < 50:
            cv2.imwrite(f"./collect/sprite/{i}.jpg", frame)
        elif 50 <= i < 75:
            cv2.imwrite(f"./collect/fanta/{i}.jpg", frame)
        elif 75 <= i < 100:
            cv2.imwrite(f"./collect/gum/{i}.jpg", frame)
        else:
            break
        i = i + 1
cap.release()
cv2.destroyAllWindows()
