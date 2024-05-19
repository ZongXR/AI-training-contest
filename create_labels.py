# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import os


classes = ['cola', 'sprite', 'fanta', 'gum']
for file in os.listdir('./VOC/Annotations'):
    tree = ET.parse(f"./VOC/Annotations/{file}")
    root = tree.getroot()
 
    for size in root.iter('size'):
        width = int(size.find('width').text)
        height = int(size.find('height').text)
 
    all_content = ''
    for obj in root.iter('object'):
        cls = obj.find('name').text
        cls_id = classes.index(cls)
 
        xmlbox = obj.find('bndbox')
        xmin = int(xmlbox.find('xmin').text)
        ymin = int(xmlbox.find('ymin').text)
        xmax = int(xmlbox.find('xmax').text)
        ymax = int(xmlbox.find('ymax').text)
 
        x = (xmin+xmax) / 2 / width
        y = (ymin+ymax) / 2 / height
        w = (xmax-xmin) / width
        h = (ymax-ymin) / height
 
        one_content = '{} {:.4f} {:.4f} {:.4f} {:.4f}'.format(cls_id, x, y, w, h)
        all_content = all_content + one_content + '\n'
 
    all_content = all_content.strip('\n')
    with open(f"./VOC/labels/{file.split('.')[0]}.txt", "w") as f:
        f.write(all_content)
