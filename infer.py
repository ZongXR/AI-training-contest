# -*- coding: utf-8 -*-
import cv2
import numpy as np


LABELS = open("./model/classes.names").read().strip().split("\n")
net = cv2.dnn.readNetFromDarknet('./model/yolov4-tiny.cfg', './model/yolov4-tiny_final.weights')
layer = net.getUnconnectedOutLayersNames()[-1]

frame = cv2.imread('test.jpg')
H, W, _ = frame.shape
blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
net.setInput(blob)
output = net.forward(layer)
boxes = []
confidences = []
classIDs = []

for detection in output:
    scores = detection[5:]
    classID = np.argmax(scores)
    confidence = scores[classID]
    box = detection[0:4] * np.array([W, H, W, H])
    centerX, centerY, width, height = box.astype("int")
    x = int(centerX - (width / 2))
    y = int(centerY - (height / 2))
    boxes.append([x, y, int(width), int(height)])
    confidences.append(float(confidence))
    classIDs.append(classID)

idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.3)
if len(idxs) > 0:
    for i in idxs.flatten():
        x, y = boxes[i][0], boxes[i][1]
        w, h = boxes[i][2], boxes[i][3]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1, lineType=cv2.LINE_AA)
        text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])
        cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, lineType=cv2.LINE_AA)
        
cv2.imshow('test.jpg', frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
