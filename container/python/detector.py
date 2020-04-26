# -*- coding: utf-8 -*-

from .utils import GetContours
from .utils import GetContourProperties
from .utils import RectsFilter

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
        contours = GetContours(image)
        if len(contours) == 0:
            self.__gameRect = None
            return False
        centerList, arcLengthList, boundRectList = GetContourProperties(contours)
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
            self.__gameRect = None
            return False
        self.__gameRect = boundRectPass[0]
        return True

    def DrawGameRect(self, image, color=(0, 241, 255), thickness=2):
        x, y, w, h = self.__gameRect
        cv.rectangle(image, (x, y), (x + w, y + h), color, thickness)

    def DetectStartButtonNormalRect(self, image, width=114, height=53, eps=10):
        contours = GetContours(image)
        if len(contours) == 0:
            self.__startButtonNormalRect = None
            return False
        centerList, arcLengthList, boundRectList = GetContourProperties(contours)
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
            self.__startButtonNormalRect = None
            return False
        self.__startButtonNormalRect = boundRectPass[0]
        return True

    def DrawStartButtonNormalRect(self, image, color=(0, 241, 255), thickness=2):
        x, y, w, h = self.__startButtonNormalRect
        cv.rectangle(image, (x, y), (x + w, y + h), color, thickness)

    def DetectPlayer(self, image):
        # TODO
        return True

    def DrawPlayer(self, image):
        # TODO
        pass

    def DetectLevel(self, image):
        # TODO
        return True

    def DrawLevel(self, image):
        # TODO
        pass

    def DetectMaskPoints(self, image, eps=10):
        # TODO
        contours = GetContours(image)
        if len(contours) == 0:
            self.__maskPoints = None
            return False
        centerList, arcLengthList, boundRectList = GetContourProperties(contours)
        contoursPass = []
        boundRectPass = []
        for contour, center, arcLength, boundRect in zip(contours, centerList, arcLengthList, boundRectList):
            if boundRect[0] < self.__gameRect[0] + eps:
                continue
            if boundRect[1] < self.__gameRect[1] + eps:
                continue
            if self.__gameRect[0] + self.__gameRect[2] < boundRect[0] + boundRect[2]:
                continue
            if self.__gameRect[1] + self.__gameRect[3] < boundRect[1] + boundRect[3]:
                continue
            contoursPass.append(contour)
            boundRectPass.append(boundRect)
        if len(contoursPass) == 0:
            self.__maskPoints = None
            return False
        self.__maskPoints = RectsFilter(rects=boundRectPass, minW=20, minH=30)
        return True

    def DrawMaskPoints(self, image, color=(0, 241, 255), thickness=2):
        for maskPoint in self.__maskPoints:
            x, y, w, h = maskPoint
            cv.rectangle(image, (x, y), (x + w, y + h), color, thickness)

    def DetectSocialDistance(self, image):
        # TODO
        return True

    def DrawSocialDistance(self, image):
        # TODO
        pass

    def DetectEnemies(self, image):
        # TODO
        return True

    def DrawEnemies(self, image):
        # TODO
        pass

    def DetectAvesans(self, image):
        # TODO
        return True

    def DrawAvesans(self, image):
        # TODO
        pass

    def DetectItems(self, image):
        # TODO
        return True

    def DrawItems(self, image):
        # TODO
        pass
