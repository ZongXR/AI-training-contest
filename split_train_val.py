# -*- coding: utf-8 -*-
import os


num = 0
train_txt = open('./model/train.txt', 'w')
val_txt = open('./model/val.txt', 'w')
for file in os.listdir('./VOC/JPEGImages'):
    num = num + 1
    if num < 100 * 0.8:    # train
        print(f"./VOC/JPEGImages/{file}", file=train_txt, flush=True)
    else:                  # test
        print(f"./VOC/JPEGImages/{file}", file=val_txt, flush=True)
val_txt.close()
train_txt.close()