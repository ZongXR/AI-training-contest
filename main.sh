#!/bin/bash
# 图像处理
mkdir -p ./Deduplication
python ./Deduplication.py
mkdir -p ./conversion
python ./conversion.py
mkdir -p ./concatenation
python ./concatenation.py
# TODO 图像采集
# TODO 图像标注
# TODO 标注结果解析
# TODO 模型调参及模型训练
# TODO 模型验证
# TODO 应用场景开发
# TODO 应用场景验证