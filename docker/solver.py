#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import cv2 as cv

from time import sleep
from PIL import Image
from Xlib.display import Display
from Xlib.X import ZPixmap
from Xlib.X import MotionNotify
from Xlib.X import ButtonPress
from Xlib.X import ButtonRelease
from Xlib.ext.xtest import fake_input

def Main():
    display, window = GetX11()
    gameRect = WaitDetection(window, DetectGameRect)
    startButtonRect = WaitDetection(window, DetectStartButtonRect, gameRect=gameRect)
    ClickStartButton(display, startButtonRect)
    RepeatSocialDistance(display, gameRect)

def GetX11():
    display = Display()
    screen = display.screen()
    window = screen.root
    return display, window

def GetImage(window, w=1024, h=768):
    rawimage = window.get_image(0, 0, w, h, ZPixmap, 0xFFFFFFFF).data
    image = Image.frombytes('RGB', (w, h), rawimage, 'raw', 'RGBX')
    return np.asarray(image)

def GetContours(image, thresh = 150):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    gray = cv.blur(gray, (3, 3))
    canny = cv.Canny(gray, thresh, thresh * 2)
    contours = cv.findContours(canny, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)[0]
    return contours

def GetContourProperties(contours):
    centerList = []
    arcLengthList = []
    boundRectList = []
    for contour in contours:
        poly = cv.approxPolyDP(contour, 3, True)
        mu = cv.moments(poly)
        cx = mu['m10'] / (mu['m00'] + 1e-5)
        cy = mu['m01'] / (mu['m00'] + 1e-5)
        centerList.append((cx, cy))
        arcLengthList.append(cv.arcLength(poly, True))
        boundRectList.append(cv.boundingRect(poly))
    return centerList, arcLengthList, boundRectList

def WaitDetection(window, detectionFn, gameRect=None):
    res = None
    while res is None:
        sleep(0.5)
        image = GetImage(window)
        res = detectionFn(image, gameRect)
    return res

def DetectGameRect(image, gameRect):
    contours = GetContours(image)
    if len(contours) == 0:
        return None
    centerList, arcLengthList, boundRectList = GetContourProperties(contours)
    contoursPass = []
    boundRectPass = []
    for contour, center, arcLength, boundRect in zip(contours, centerList, arcLengthList, boundRectList):
        if arcLength < 1500 or 2000 < arcLength:
            continue
        if center[0] < 400 or 500 < center[0]:
            continue
        if center[1] < 300 or 400 < center[1]:
            continue
        if abs(boundRect[2] - 400) > 10:
            continue
        if abs(boundRect[3] - 500) > 10:
            continue
        contoursPass.append(contour)
        boundRectPass.append(boundRect)
    if len(contoursPass) == 0:
        return None
    return boundRectPass[0]

def DetectStartButtonRect(image, gameRect):
    contours = GetContours(image)
    if len(contours) == 0:
        return None
    centerList, arcLengthList, boundRectList = GetContourProperties(contours)
    contoursPass = []
    boundRectPass = []
    for contour, center, arcLength, boundRect in zip(contours, centerList, arcLengthList, boundRectList):
        if boundRect[0] < gameRect[0]:
            continue
        if boundRect[1] < gameRect[1]:
            continue
        if gameRect[0] + gameRect[2] < boundRect[0] + boundRect[2]:
            continue
        if gameRect[1] + gameRect[3] < boundRect[1] + boundRect[3]:
            continue
        if center[0] < gameRect[0] + gameRect[2] / 2.0:
            continue
        if center[1] < gameRect[1] + gameRect[3] / 2.0:
            continue
        if arcLength < 300 or 1000 < arcLength:
            continue
        contoursPass.append(contour)
        boundRectPass.append(boundRect)
    if len(contoursPass) == 0:
        return None
    return boundRectPass[0]

def Click(display, x, y, duration=1.0):
    fake_input(display, MotionNotify, x=int(x), y=int(y))
    fake_input(display, ButtonPress, 1)
    display.sync()
    sleep(duration)
    fake_input(display, ButtonRelease, 1)
    display.sync()

def ClickStartButton(display, startButtonRect):
    x = startButtonRect[0] + startButtonRect[2] / 2.0
    y = startButtonRect[1] + startButtonRect[3] / 2.0
    Click(display, x, y)

def RepeatSocialDistance(display, gameRect):
    x = gameRect[0] + gameRect[2] / 2.0
    y = gameRect[1] + gameRect[3] / 2.0
    while True:
        Click(display, x, y)

if __name__ == '__main__':
    Main()
