# -*- coding: utf-8 -*-
import os
import numpy as np
import cv2


for file in os.listdir("./data/"):
    frame = cv2.imread(f"./data/{file}", cv2.IMREAD_COLOR)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    frame = frame.astype(np.uint8)
    cv2.imwrite(f"./data/{file}", frame)
