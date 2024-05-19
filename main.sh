#!/bin/bash
# 图像采集与处理
python ./clean.py
python ./gather.py
mkdir -p ./images
cp -rf ./data/*.jpg ./images/
cp -rf ./collect/*.jpg ./images/
# 图像标注
mkdir -p ./Annotation
mkdir -p ./VOC/Annotations
mkdir -p ./VOC/JPEGImages
labelimg ./images/ ./classes.names
cp -rf ./Annotation/*.xml ./VOC/Annotations/
cp -rf ./images/*.jpg ./VOC/JPEGImages