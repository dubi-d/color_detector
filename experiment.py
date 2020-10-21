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


def build_color_histogram(img):
    """
    Categorize each pixel into color bins and build a histogram.

    :param img: input image
    :return: histogram of frequent colors in image
    """
    color_hist = {"red": 0,
                  "yellow": 0,
                  "green": 0,
                  "cyan": 0,
                  "blue": 0,
                  "purple": 0}
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV_FULL)
    [height, width, _] = img_hsv.shape
    for y in range(height):
        for x in range(width):
            pixel_color = hue_to_color_name(img_hsv[y, x, 0])
            color_hist[pixel_color] += 1
    return color_hist


def most_frequent(color_hist):
    """
    Extract the most frequet color from the color histogram.

    :param color_hist: color histogram
    :return: key of the max value in color_hist
    """
    return max(color_hist, key=color_hist.get)


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

    avg_colors_bgr = []
    frequent_colors = []
    for seg in segments:
        avg_colors_bgr.append(average_color(seg))
        hist = build_color_histogram(seg)
        frequent_colors.append(most_frequent(hist))

    for i in range(N_SPLITS):
        hsv = cv2.cvtColor(avg_colors_bgr[i], cv2.COLOR_BGR2HSV_FULL)
        print(f"Split {i}    average: {hue_to_color_name(hsv[0, 0, 0])} (hue={hsv[0, 0, 0]}), "
              f"most frequent: {frequent_colors[i]}")

    if DEBUG:
        display_image_segments(frame, avg_colors_bgr, N_SPLITS)
