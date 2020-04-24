# -*- coding: utf-8 -*-

import cv2 as cv

class Detector(object):

    def __init__(self, x11):
        self.__x11 = x11
        self.__gameRect = None

    def __GetContours(self, thresh=150):
        gray = cv.cvtColor(self.__image, cv.COLOR_BGR2GRAY)
        gray = cv.blur(gray, (3, 3))
        canny = cv.Canny(gray, thresh, thresh * 2)
        contours = cv.findContours(canny, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)[0]
        return contours

    def __GetContourProperties(self):
        centerList = []
        arcLengthList = []
        boundRectList = []
        contours = self.__GetContours()
        for contour in contours:
            poly = cv.approxPolyDP(contour, 3, True)
            mu = cv.moments(poly)
            cx = mu['m10'] / (mu['m00'] + 1e-5)
            cy = mu['m01'] / (mu['m00'] + 1e-5)
            centerList.append((cx, cy))
            arcLengthList.append(cv.arcLength(poly, True))
            boundRectList.append(cv.boundingRect(poly))
        return centerList, arcLengthList, boundRectList

    def DetectGameRect(self):
        contours = self.__GetContours()
        if len(contours) == 0:
            return None
        centerList, arcLengthList, boundRectList = self.__GetContourProperties()
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

    def DetectStartButtonRect(image):
        contours = self.__GetContours()
        if len(contours) == 0:
            return None
        centerList, arcLengthList, boundRectList = self.__GetContourProperties()
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
