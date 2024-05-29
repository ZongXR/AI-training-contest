# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import os
from PIL import Image, ImageDraw, ImageFont


classes = open("./model/classes.names").read().strip().split("\n")
for file in os.listdir('./VOC/Annotations'):
    tree = ET.parse(f"./VOC/Annotations/{file}")
    root = tree.getroot()

    image = Image.open(f"./VOC/JPEGImages/{file.split('.')[0] + '.jpg'}")
    draw = ImageDraw.Draw(image)
    for obj in root.iter('object'):
        cls = obj.find('name').text

        xmlbox = obj.find('bndbox')
        xmin = int(xmlbox.find('xmin').text)
        ymin = int(xmlbox.find('ymin').text)
        xmax = int(xmlbox.find('xmax').text)
        ymax = int(xmlbox.find('ymax').text)

        draw.rectangle([(xmin, ymin), (xmax, ymax)], outline=(255, 0, 0), width=1)
        draw.text((xmin, ymin), cls, font=ImageFont.truetype('arial.ttf', 36), fill=(0, 0, 255))
    image.save(f"./analysisImage/{file.split('.')[0] + '.jpg'}")
