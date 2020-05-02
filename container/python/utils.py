# -*- coding: utf-8 -*-

import cv2 as cv
import numpy as np

from os import listdir
from os import path
from glob import glob

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

def CreateRectGroups(rects, minW, minH):
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

def RemoveFloor(image, hsvMin=(0, 0, 185), hsvMax=(0, 0, 195)):
    hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    mask = 255 - cv.inRange(hsv, hsvMin, hsvMax)
    return cv.bitwise_and(image, image, None, mask)

def RemoveSocialDistance(image, hsvMin=(40, 0, 0), hsvMax=(45, 255, 255)):
    hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    mask = 255 - cv.inRange(hsv, hsvMin, hsvMax)
    return cv.bitwise_and(image, image, None, mask)

def ExtractSocialDistance(image, hsvMin=(40, 0, 0), hsvMax=(45, 255, 255)):
    hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    mask = cv.inRange(hsv, hsvMin, hsvMax)
    return cv.bitwise_and(image, image, None, mask)

def GetHogDescriptor(winSize=(20, 20),
                     blockSize=(10, 10),
                     blockStride=(5, 5),
                     cellSize=(10, 10),
                     nbins=9,
                     derivAperture=1,
                     winSigma=-1,
                     histogramNormType=0,
                     L2HysThreshold=0.2,
                     gammaCorrection=1,
                     nlevels=64,
                     useSignedGradients=True):
    return cv.HOGDescriptor(winSize, blockSize, blockStride,
                            cellSize, nbins, derivAperture,
                            winSigma, histogramNormType, L2HysThreshold,
                            gammaCorrection, nlevels, useSignedGradients)

def ResizeHog(image, w=64, h=128):
    return cv.resize(image, (w, h))

def GetTrainedSvm():
    data = []
    dataTypes = []
    dataDir = path.join('/', 'data')
    for i, subdir in enumerate(listdir(dataDir)):
        dataTypes.append(subdir)
        data.append([])
        for dataPath in glob(path.join(dataDir, subdir, '*.png')):
            image = cv.imread(dataPath)
            image = RemoveFloor(image)
            image = RemoveSocialDistance(image)
            data[i].append(image)

    hog = GetHogDescriptor()
    descriptors = []
    for i, images in enumerate(data):
        descriptors.append([])
        for image in images:
            resized = ResizeHog(image)
            descriptors[i].append(hog.compute(resized))

    trainLabels = []
    trainDescriptors = []
    for label, descriptor in enumerate(descriptors):
        for des in descriptor:
            trainLabels.append(label)
            trainDescriptors.append(des)
    trainLabels = np.array(trainLabels)
    trainDescriptors = np.array(trainDescriptors)

    svm = cv.ml.SVM_create()
    svm.trainAuto(trainDescriptors, cv.ml.ROW_SAMPLE, trainLabels)
    return svm, dataTypes

def GetRectCenter(rect):
    x, y, w, h = rect
    return x + w / 2.0, y + h / 2.0

def IsIntersected(line1, line2, eps=1e-7):
    a1 = np.array(line1[0])
    a2 = np.array(line1[1])
    b1 = np.array(line2[0])
    b2 = np.array(line2[1])
    if abs(np.cross(a2 - a1, b2 - b1)) < eps:
        return False
    if np.cross(a2 - a1, b1 - a1) * np.cross(a2 - a1, b2 - a1) > eps:
        return False
    if np.cross(b2 - b1, a1 - b1) * np.cross(b2 - b1, a2 - b1) > eps:
        return False
    return True

def GetIntersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / float(div)
    y = det(d, ydiff) / float(div)
    return x, y

def GetPointDistance(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.linalg.norm(a - b)

def GetRectDistance(rect1, rect2):
    if RectIsIntersected(rect1, rect2):
        return 0.0
    c1 = GetRectCenter(rect1)
    c2 = GetRectCenter(rect2)
    intersections = []
    for rect in [rect1, rect2]:
        x, y, w, h = rect
        a = (x, y)
        b = (x, y + h)
        c = (x + w, y + h)
        d = (x + w, y)
        for line in [(a, b), (b, c), (c, d), (d, a)]:
            if not IsIntersected(line, (c1, c2)):
                continue
            intersected = line
            break
        intersection = GetIntersection(intersected, (c1, c2))
        intersections.append(intersection)
    distance = GetPointDistance(*intersections)
    return distance
