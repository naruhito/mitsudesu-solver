# -*- coding: utf-8 -*-

import cv2 as cv

def GetContours(image, thresh=150):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    grayBlur = cv.blur(gray, (3, 3))
    canny = cv.Canny(grayBlur, thresh, thresh * 2)
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
        center = (cx, cy)
        arcLength = cv.arcLength(poly, True)
        boundRect = cv.boundingRect(poly)
        centerList.append(center)
        arcLengthList.append(arcLength)
        boundRectList.append(boundRect)
    return centerList, arcLengthList, boundRectList

def RectsFilter(rects, minW, minH):
    res = []
    while len(rects) > 0:
        rect = rects.pop(0)
        while True:
            changed = False
            rectsUnused = []
            for rect2 in rects:
                if not RectIsIntersected(rect, rect2):
                    rectsUnused.append(rect2)
                    continue
                if rect[2] > minW and rect[3] > minH:
                    res.append(rect)
                if rect2[2] > minW and rect2[3] > minH:
                    res.append(rect2)
                rect = RectUnite(rect, rect2)
                changed = True
            rects = rectsUnused
            if not changed:
                break
        res.append(rect)
    return res

def RectIsIntersected(a, b):
    x = max(a[0], b[0])
    y = max(a[1], b[1])
    w = min(a[0] + a[2], b[0] + b[2]) - x
    h = min(a[1] + a[3], b[1] + b[3]) - y
    if w < 0 or h < 0:
        return False
    return True

def RectUnite(a, b):
    x = min(a[0], b[0])
    y = min(a[1], b[1])
    w = max(a[0] + a[2], b[0] + b[2]) - x
    h = max(a[1] + a[3], b[1] + b[3]) - y
    return x, y, w, h
