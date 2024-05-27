# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import os
import cv2


classes = open("./model/classes.names").read().strip().split("\n")
for file in os.listdir('./VOC/Annotations'):
    tree = ET.parse(f"./VOC/Annotations/{file}")
    root = tree.getroot()

    frame = cv2.imread(f"./VOC/JPEGImages/{file.split('.')[0] + '.jpg'}", cv2.IMREAD_COLOR)
    for obj in root.iter('object'):
        cls = obj.find('name').text

        xmlbox = obj.find('bndbox')
        xmin = int(xmlbox.find('xmin').text)
        ymin = int(xmlbox.find('ymin').text)
        xmax = int(xmlbox.find('xmax').text)
        ymax = int(xmlbox.find('ymax').text)

        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 0, 255), 1, cv2.LINE_AA)
        cv2.putText(frame, cls, (xmin, ymin), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
    cv2.imwrite(f"./analysisImage/{file.split('.')[0] + '.jpg'}", frame)
