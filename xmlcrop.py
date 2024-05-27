# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import os
import cv2


classes = open("./model/classes.names").read().strip().split("\n")
nums = {x: 0 for x in classes}
for file in os.listdir('./VOC/Annotations'):
    tree = ET.parse(f"./VOC/Annotations/{file}")
    root = tree.getroot()

    frame = cv2.imread(f"./VOC/JPEGImages/{file.split('.')[0] + '.jpg'}", cv2.IMREAD_COLOR)
    for obj in root.iter('object'):
        cls = obj.find('name').text
        if not os.path.exists(f"./crop/{cls}"):
            os.mkdir(f"./crop/{cls}")

        xmlbox = obj.find('bndbox')
        xmin = int(xmlbox.find('xmin').text)
        ymin = int(xmlbox.find('ymin').text)
        xmax = int(xmlbox.find('xmax').text)
        ymax = int(xmlbox.find('ymax').text)

        cropped = frame[xmin:xmax + 1, ymin:ymax + 1].copy()
        cv2.imwrite(f"./crop/{cls}/{nums[cls]}.jpg", cropped)
        nums[cls] = nums[cls] + 1
