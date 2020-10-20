#!/usr/bin/env python3
import cv2
import numpy as np
from time import sleep

cap = cv2.VideoCapture(2)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    #Put here your code!
    # You can now treat output as a normal numpy array
    # Do your magic here

    sleep(1)
