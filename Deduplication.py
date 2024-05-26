# -*- coding: utf-8 -*-
import os
import cv2


def calculate_hash(image):
    image = cv2.resize(image, (9, 8), interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    hash_value = 0
    for i in range(8):
        for j in range(8):
            if gray[i, j] > gray[i, j + 1]:
                hash_value += 1 << (i * 8 + j)
    return hash_value


hash_set = set()
for file in os.listdir("./data/"):
    frame = cv2.imread(f"./data/{file}", cv2.IMREAD_COLOR)
    img_hash = calculate_hash(frame)
    if img_hash not in hash_set:
        hash_set.add(img_hash)
        cv2.imwrite(f"./Deduplication/{file}", frame)
