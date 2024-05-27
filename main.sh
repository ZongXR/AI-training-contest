#!/bin/bash
# 图像处理
mkdir -p ./Deduplication
python ./Deduplication.py
mkdir -p ./conversion
python ./conversion.py
mkdir -p ./concatenation
python ./concatenation.py
# 图像采集
python ./gather.py
mkdir -p ./images
cp -rf ./conversion/*.jpg ./images/
cp -rf ./collect/*.jpg ./images/
# 图像标注
mkdir -p ./Annotations
mkdir -p ./VOC
labelimg ./images/ ./model/classes.names
cp -rf ./Annotations ./VOC/
cp -rf ./images ./VOC/JPEGImages
# 标注结果解析
mkdir -p ./analysisImage
python ./xmlanalysis.py
# TODO 标注结果裁剪
# TODO 模型调参及模型训练
# TODO 模型验证
# TODO 应用场景开发
# TODO 应用场景验证