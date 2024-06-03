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
labelimg ./images/ ./model/classes.names
cp -rf ./Annotation/*.xml ./VOC/Annotations/
cp -rf ./images/*.jpg ./VOC/JPEGImages/
# 模型调参及模型训练
mkdir -p ./VOC/labels
python ./create_labels.py
python ./get_train_val.py
darknet_path=$(dirname $(which darknet))
cd ${darknet_path}
if [[ "OPENCV=1" != "$(sed -n '4,1p' Makefile)" ]];then
  echo "recompile darknet..."
  sed -i "4c OPENCV=1" Makefile
  make
fi
cd -
darknet detector train ./model/custom_training.data ./model/yolov4-tiny.cfg ./model/yolov4-tiny.conv.29
# 模型验证
python ./infer.py
# 应用场景开发与验证
sudo python ./control.py
sudo python ./retail.py
