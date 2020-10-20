#!/usr/bin/env python3
import cv2
import numpy as np
from time import sleep
import os


#N_SPLITS = int(os.environ['N_SPLITS'])
N_SPLITS = 3
print("N_SPLITS = ", N_SPLITS)

# cap = cv2.VideoCapture(2)
img = cv2.imread("testimg.jpg")

frame_width = 320
frame_height = 240
frame = cv2.resize(img, (frame_width, frame_height))
print("frame shape", frame.shape)  # shape is height, width, channels
frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

segment_height = 1.0 * frame_height / N_SPLITS


colors_hsv = []
blurred = frame.copy()
blur_x = int(frame_width / 2)
blur_x += (blur_x+1) % 2
blur_y = int(segment_height / 2)
blur_y += (blur_y+1) % 2
blur_level = 10

for i in range(N_SPLITS):
    seg = frame[int(i*segment_height):int((i+1)*segment_height), :]  # split up image
    print("seg shape", seg.shape)
    blur = cv2.GaussianBlur(seg, (blur_x, blur_y), 0)
    for k in range(blur_level):
        blur = cv2.GaussianBlur(blur, (blur_x, blur_y), 0)
    print("blur shape", blur.shape)
    colors_hsv.append(blur[int(segment_height/2), int(frame_width/2)])  # pick out center pixel
    print(colors_hsv)
    blurred[int(i*segment_height):int((i+1)*segment_height), :] = blur

# categorize by hue value of center pixel
for i in range(N_SPLITS):
    print(f"Split {i} dominant hue: {colors_hsv[i][0]}")

cv2.namedWindow("image1")
cv2.namedWindow("image2")
cv2.imshow("image1", frame)
cv2.imshow("image2", blurred)
cv2.waitKey(0)
