#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import cv2 as cv

from Xlib.display import Display
from Xlib.X import ZPixmap
from PIL import Image
from numpy import asarray

display = Display()
screen = display.screen()
window = screen.root

# import IPython; IPython.embed()

rawimage = window.get_image(0, 0, 1024, 768, ZPixmap, 0xFFFFFFFF).data
image = Image.frombytes('RGB', (1024, 768), rawimage, 'raw', 'RGBX')

from time import sleep
sleep(5)
with open('./bbb.png', 'wb') as f:
    Image.fromarray(asarray(image)).save(f, 'PNG')

from Xlib.display import Display
from Xlib.X import MotionNotify
from Xlib.X import ButtonPress
from Xlib.X import ButtonRelease
from Xlib.ext.xtest import fake_input

# fake_input(display, MotionNotify, x=100, y=200)
# fake_input(display, ButtonPress, 1)
# display.sync()

# fake_input(display, ButtonRelease, 1)
# display.sync()



img = cv.imread('bbb.png')
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
gray = cv.blur(gray, (3,3))
thresh = 150
canny = cv.Canny(gray, thresh, thresh * 2)
contours, _ = cv.findContours(canny, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

contours_poly = []
boundRect = [None]*len(contours)
for i, contour in enumerate(contours):
    poly = cv.approxPolyDP(contour, 3, True)
    contours_poly.append(poly)
    boundRect[i] = cv.boundingRect(contours_poly[i])

dstContoursPoly = np.zeros((canny.shape[0], canny.shape[1], 3), dtype=np.uint8)
for i in range(len(contours)):
    color = [255, 0, 0]
    # cv.drawContours(dstContoursPoly, contours_poly, i, color)
    cv.rectangle(dstContoursPoly, (int(boundRect[i][0]), int(boundRect[i][1])),
                 (int(boundRect[i][0]+boundRect[i][2]), int(boundRect[i][1]+boundRect[i][3])), color, 2)

cv.imshow('dst', dstContoursPoly)
cv.waitKey(0)
