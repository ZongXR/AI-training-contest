# -*- coding: utf-8 -*-
import numpy as np
import cv2


frame = cv2.imread("./test.jpg", cv2.IMREAD_COLOR)
frame_cvt = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
result = np.concatenate([frame, frame_cvt], axis=1)
result = np.tile(result, (3, 1, 1))
cv2.imshow("concatenation", result)
while True:
    k = cv2.waitKey(1)
    if k == ord(" "):
        cv2.imwrite("./concatenation/test.jpg", result)
        cv2.destroyAllWindows()
        break
