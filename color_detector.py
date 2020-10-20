#!/usr/bin/env python3
import cv2
import numpy as np
from time import sleep
import os


N_SPLITS = int(os.environ["N_SPLITS"])

cap = cv2.VideoCapture(2)

frame_width = cap.get(3)
frame_height = cap.get(4)
segment_height = 1.0 * frame_height / N_SPLITS

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Put here your code!
    # You can now treat output as a normal numpy array
    # Do your magic here
    if not ret:
        continue

    colors_bgr = np.zeros((N_SPLITS, 3))
    for i in range(N_SPLITS):
        seg = frame[int(i*segment_height):int((i+1)*segment_height), :]  # split up image
        blur = cv2.GaussianBlur(seg, (segment_height/2, frame_width/2), 0)
        colors_bgr[i, :] = blur[segment_height/2, frame_width/2, :]  # pick out center pixel

    # categorize by hue value of center pixel
    colors_hsv = cv2.cvtColor(colors_bgr, cv2.COLOR_BGR2HSV)
    for i in range(N_SPLITS):
        print(f"Split {i} dominant hue: {colors_hsv[0, 0]}")

    sleep(1)
