# -*- coding: utf-8 -*-
import cv2
import numpy as np
from control import *


LABELS = open("./model/classes.names").read().strip().split("\n")
net = cv2.dnn.readNetFromDarknet('./model/yolov4-tiny.cfg', './model/yolov4-tiny_final.weights')
layer = net.getUnconnectedOutLayersNames()[-1]
cap = cv2.VideoCapture(0)
qr = cv2.QRCodeDetector()
change_screen_command("page 7")

i = 0
while True:
    ret, frame = cap.read()
    if ret:
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
                label = LABELS[classIDs[i]]
                text = "{}: {:.4f}".format(label, confidences[i])
                if label == "gum":
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1, lineType=cv2.LINE_AA)
                    cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, lineType=cv2.LINE_AA)
                else:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1, lineType=cv2.LINE_AA)
                    cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, lineType=cv2.LINE_AA)

        cv2.imshow("capture", frame)
        send_screen_information_command("t71.txt", classIDs.count(1))     # sprite
        send_screen_information_command("t72.txt", classIDs.count(0))     # cola
        send_screen_information_command("t73.txt", classIDs.count(2))     # fanta
        send_screen_information_command("t707.txt", classIDs.count(3))    # gum
        send_screen_information_command("t713.txt", len(classIDs))        # number
        send_screen_information_command("t714.txt", classIDs.count(1) * 3 + classIDs.count(0) * 2 + classIDs.count(2) * 8 + classIDs.count(3) * 2)
        if "Z1" == wait_screen("m70"):
            data, bbox, qrcode = qr.detectAndDecode(frame)
            while len(data) == 0:
                cv2.imshow("capture", frame)
                data, bbox, qrcode = qr.detectAndDecode(frame)
            for box in bbox:
                cv2.line(frame, tuple(box[0].astype(int)), tuple(box[1].astype(int)), (255, 0, 0), 2)
                cv2.line(frame, tuple(box[1].astype(int)), tuple(box[2].astype(int)), (255, 0, 0), 2)
                cv2.line(frame, tuple(box[2].astype(int)), tuple(box[3].astype(int)), (255, 0, 0), 2)
                cv2.line(frame, tuple(box[3].astype(int)), tuple(box[0].astype(int)), (255, 0, 0), 2)
            cv2.imshow("capture", frame)
            print("二维码信息:", data)
            change_screen_command("page main")
            not_screen_and_sensor_command("C-!")

    k = cv2.waitKey(1)
    if k == ord(' '):
        break
cv2.destroyAllWindows()
