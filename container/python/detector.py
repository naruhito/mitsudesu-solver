# -*- coding: utf-8 -*-

import cv2 as cv

class Detector(object):

    def __init__(self):
        self.__gameRect = None
        self.__startButtonNormalRect = None
        self.__player = None
        self.__level = None
        self.__maskPoints = None
        self.__socialDistance = None
        self.__enemies = None
        self.__avesans = None
        self.__items = None

    def GetGameRect(self):
        return self.__gameRect

    def GetStartButtonNormalRect(self):
        return self.__startButtonNormalRect

    def GetPlayer(self):
        return self.__player

    def GetLevel(self):
        return self.__level

    def GetMaskPoints(self):
        return self.__maskPoints

    def GetSocialDistance(self):
        return self.__socialDistance

    def GetEnemies(self):
        return self.__enemies

    def GetAvesans(self):
        return self.__avesans

    def GetItems(self):
        return self.__items

    def DetectGameRect(self, image, width=400, height=500, eps=10):
        contours = self.__GetContours(image)
        if len(contours) == 0:
            return False
        centerList, arcLengthList, boundRectList = self.__GetContourProperties(contours)
        contoursPass = []
        boundRectPass = []
        for contour, center, arcLength, boundRect in zip(contours, centerList, arcLengthList, boundRectList):
            if abs(boundRect[2] - width) > eps:
                continue
            if abs(boundRect[3] - height) > eps:
                continue
            contoursPass.append(contour)
            boundRectPass.append(boundRect)
        if len(contoursPass) == 0:
            return False
        self.__gameRect = boundRectPass[0]
        return True

    def DetectStartButtonNormalRect(self, image, width=114, height=53, eps=10):
        contours = self.__GetContours(image)
        if len(contours) == 0:
            return False
        centerList, arcLengthList, boundRectList = self.__GetContourProperties(contours)
        contoursPass = []
        boundRectPass = []
        for contour, center, arcLength, boundRect in zip(contours, centerList, arcLengthList, boundRectList):
            if boundRect[0] < self.__gameRect[0]:
                continue
            if boundRect[1] < self.__gameRect[1]:
                continue
            if self.__gameRect[0] + self.__gameRect[2] < boundRect[0] + boundRect[2]:
                continue
            if self.__gameRect[1] + self.__gameRect[3] < boundRect[1] + boundRect[3]:
                continue
            if center[0] < self.__gameRect[0] + self.__gameRect[2] / 2.0:
                continue
            if center[1] < self.__gameRect[1] + self.__gameRect[3] / 2.0:
                continue
            if abs(boundRect[2] - width) > eps:
                continue
            if abs(boundRect[3] - height) > eps:
                continue
            contoursPass.append(contour)
            boundRectPass.append(boundRect)
        if len(contoursPass) == 0:
            return False
        self.__startButtonNormalRect = boundRectPass[0]
        return True

    def DetectPlayer(self, image):
        # TODO
        return True

    def DetectLevel(self, image):
        # TODO
        return True

    def DetectMaskPoints(self, image):
        # TODO
        return True

    def DetectSocialDistance(self, image):
        # TODO
        return True

    def DetectEnemies(self, image):
        # TODO
        return True

    def DetectAvesans(self, image):
        # TODO
        return True

    def DetectItems(self, image):
        # TODO
        return True

    def __GetContours(self, image, thresh=150):
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        grayBlur = cv.blur(gray, (3, 3))
        canny = cv.Canny(grayBlur, thresh, thresh * 2)
        contours = cv.findContours(canny, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)[0]
        return contours

    def __GetContourProperties(self, contours):
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
