#!/usr/bin/env python3
import cv2
import numpy as np
from time import sleep
import os


def split_image(img, n):
    """
    Split up the image into n horizontal segments of equal height.

    :param img: Input image
    :param n: Number of segments
    :return: List of image segments
    """
    [height, width, _] = img.shape
    segment_height = 1.0 * height / n
    segments = []
    for i in range(n):
        seg = frame[int(i * segment_height):int((i + 1) * segment_height), :]  # split up image
        segments.append(seg)
    return segments


def average_color(img):
    """
    Compute average pixel values of each channel
    :param img: Input image
    :return: average value of each channel
    """
    per_row = np.average(img, axis=0)
    avg = np.average(per_row, axis=0)
    return np.uint8([[[avg[0], avg[1], avg[2]]]])


def hue_to_color_name(hue_value):
    if (0 <= hue_value <= 30) or (330 < hue_value <= 360):
        return "red"
    elif 30 < hue_value <= 90:
        return "yellow"
    elif 90 < hue_value <= 150:
        return "green"
    elif 150 < hue_value <= 210:
        return "cyan"
    elif 210 < hue_value <= 270:
        return "blue"
    elif 270 < hue_value <= 330:
        return "purple"


def display_image_segments(img, colors, n):
    [height, width, _] = img.shape
    segment_height = 1.0 * height / n
    dominant_colors = np.zeros(img.shape, np.uint8)
    for i in range(n):
        dominant_colors[int(i * segment_height):int((i + 1) * segment_height), :] = colors[i]
    cv2.imshow("Dominant Color", np.hstack([img, dominant_colors]))
    cv2.waitKey(0)


if __name__ == "__main__":
    #N_SPLITS = int(os.environ['N_SPLITS'])
    N_SPLITS = 3
    DEBUG = True

    # cap = cv2.VideoCapture(2)
    img = cv2.imread("testimg.jpg")

    frame_width = 320
    frame_height = 240
    frame = cv2.resize(img, (frame_width, frame_height))

    segments = split_image(frame, N_SPLITS)

    colors_bgr = []
    for seg in segments:
        colors_bgr.append(average_color(seg))

    # categorize by hue value of center pixel
    for i in range(N_SPLITS):
        print(colors_bgr[i].shape)
        print(colors_bgr[i][0], "this")
        hsv = cv2.cvtColor(colors_bgr[i], cv2.COLOR_BGR2HSV_FULL)
        print(f"Split {i} dominant color: {hue_to_color_name(hsv[0, 0, 0])} (hue={hsv[0, 0, 0]})")

    if DEBUG:
        display_image_segments(frame, colors_bgr, N_SPLITS)
