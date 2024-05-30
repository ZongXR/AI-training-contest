# -*- coding: utf-8 -*-
import time
import cv2
import numpy as np
from threading import Thread
from queue import Queue
from control import *


LABELS = open("./model/classes.names").read().strip().split("\n")
net = cv2.dnn.readNetFromDarknet("./model/yolov7-tiny.cfg", "./model/yolov7-tiny_final.weights")
layer = net.getUnconnectedOutLayersNames()[-1]
cap = cv2.VideoCapture(0)
qr = cv2.QRCodeDetector()
detect_results = Queue()
frame_queue = Queue()


def detect_objects(frame):
    """
    对一张图片进行目标检测\n
    :param frame: RGB图片
    :return: boxes, confidences, class_ids
    """
    height, width, _ = frame.shape
    blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    output = net.forward(layer)
    boxes = []
    confidences = []
    class_ids = []
    for detection in output:
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]
        box = detection[0:4] * np.array([width, height, width, height])
        center_x, center_y, box_width, box_height = box.astype(int)
        x = int(center_x - box_width / 2)
        y = int(center_y - box_height / 2)
        boxes.append([x, y, int(box_width), int(box_height)])
        confidences.append(confidence)
        class_ids.append(class_id)
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.3)
    return [boxes[i] for i in idxs], [confidences[i] for i in idxs], [class_ids[i] for i in idxs]


def put_boxes(frame, boxes, confidences, class_ids):
    """
    再图片上画出目标检测框
    :param frame: 图片
    :param boxes: 目标检测框
    :param confidences: 置信度
    :param class_ids: 类别id
    :return:
    """
    for i, box in enumerate(boxes):
        x, y, w, h = box
        confidence = confidences[i]
        class_id = class_ids[i]
        label = LABELS[class_id]
        text = "{}: {:.4f}".format(label, confidence)
        if label == "gum":
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1, lineType=cv2.LINE_AA)
            cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, lineType=cv2.LINE_AA)
        else:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1, lineType=cv2.LINE_AA)
            cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, lineType=cv2.LINE_AA)


def detect_thread():
    """
    目标检测的线程，主要实现的5秒确定识别\n
    :return:
    """
    prev_boxes = None
    start_time = None
    while not frame_queue.empty():
        frame = frame_queue.get()
        current_boxes, confidences, class_ids = detect_objects(frame)
        put_boxes(frame, current_boxes, confidences, class_ids)
        cv2.imshow("capture", frame)

        if prev_boxes is None:
            prev_boxes = current_boxes
        else:
            if start_time is None:
                start_time = time.time()
            else:
                if prev_boxes == current_boxes:
                    if time.time() - start_time >= 5:
                        detect_results.put((current_boxes, confidences, class_ids))
                        if class_ids:
                            cv2.imwrite("./result.jpg", frame)
                        return
                else:
                    start_time = time.time()


def set_nums(item_nums: dict):
    """
    根据数量设置串口屏\n
    :param item_nums: 每个商品的数量
    :return:
    """
    send_screen_information_command(f"t71.txt", item_nums["sprite"])
    send_screen_information_command(f"t72.txt", item_nums["cola"])
    send_screen_information_command(f"t73.txt", item_nums["fanta"])
    send_screen_information_command(f"t707.txt", item_nums["gum"])


nums = {
    "cola": 99,
    "sprite": 99,
    "fanta": 99,
    "gum": 99
}
thread = Thread(target=detect_thread)
while True:
    change_screen_command("page 7")
    set_nums(nums)
    ret, img = cap.read()
    if ret:
        frame_queue.put(img)
        thread.start()
        thread.join()
        boxes, confidences, class_ids = detect_results.get()

        num_cola = class_ids.count(0)
        num_sprite = class_ids.count(1)
        num_fanta = class_ids.count(2)
        num_gum = class_ids.count(3)
        send_screen_information_command("t713.txt", len(class_ids))        # number
        send_screen_information_command("t714.txt", num_sprite * 3 + num_cola * 2 + num_fanta * 8 + num_gum * 2)

        if "Z1" == wait_screen("m70"):
            data, bbox, qrcode = qr.detectAndDecode(img)
            while len(data) == 0:
                cv2.imshow("capture", img)
                data, bbox, qrcode = qr.detectAndDecode(img)
            for box in bbox:
                cv2.line(img, tuple(box[0].astype(int)), tuple(box[1].astype(int)), (255, 0, 0), 2)
                cv2.line(img, tuple(box[1].astype(int)), tuple(box[2].astype(int)), (255, 0, 0), 2)
                cv2.line(img, tuple(box[2].astype(int)), tuple(box[3].astype(int)), (255, 0, 0), 2)
                cv2.line(img, tuple(box[3].astype(int)), tuple(box[0].astype(int)), (255, 0, 0), 2)
            cv2.imshow("capture", img)
            print("二维码信息:", data)
            nums["cola"] = nums["cola"] - num_cola
            nums["sprite"] = nums["sprite"] - num_sprite
            nums["fanta"] = nums["fanta"] - num_fanta
            nums["gum"] = nums["gum"] - num_gum
            not_screen_and_sensor_command("C-!")

    k = cv2.waitKey(1)
    if k == ord(" "):
        break
