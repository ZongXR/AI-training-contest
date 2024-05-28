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
# 标注结果裁剪
mkdir -p ./crop
python ./xmlcrop.py
# 模型调参及模型训练
mkdir -p ./VOC/labels
python ./split_train_val.py
python ./create_labels.py
darknet_path=$(dirname $(which darknet))
cd ${darknet_path}
if [[ "OPENCV=1" != "$(sed -n '4,1p' Makefile)" ]];then
  echo "recompile darknet..."
  sed -i "4c OPENCV=1" Makefile
  make
fi
cd -
darknet detector train ./model/custom_training.data ./model/yolov7-tiny.cfg ./model/yolov7-tiny.conv.87 > training.log
# 模型验证
python ./infer.py
# TODO 应用场景开发
# TODO 应用场景验证