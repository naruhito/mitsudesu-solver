# -*- coding: utf-8 -*-

from .utils import GetContours
from .utils import GetContourProperties
from .utils import CreateRectGroups
from .utils import RemoveFloor
from .utils import CreateSvm
from .utils import CreateHog

import cv2 as cv
import numpy as np

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
        self.__svm = CreateSvm()
        self.__hog = CreateHog()

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
        objectRects = self.__DetectObjects(image)
        if objectRects is None:
            self.__player = None
            return False
        descriptors = []
        for objectRect in objectRects:
            x, y, w, h = objectRect
            roi = RemoveFloor(image[y:(y + h), x:(x + w)])
            roi = cv.resize(roi, (64, 128))
            des = self.__hog.compute(roi)
            descriptors.append(des)
        predictions = self.__svm[0].predict(np.array(descriptors))[1]
        dataTypes = self.__svm[1]
        candidates = []
        for objectRect, prediction in zip(objectRects, predictions):
            prediction = dataTypes[int(prediction[0])]
            if prediction == 'player':
                candidates.append(objectRect)
        if len(candidates) == 0:
            self.__player = None
            return False
        for candidate in candidates:
            x, y, w, h = candidate
            if y < self.__gameRect[1] + self.__gameRect[3] / 2.0:
                continue
            self.__player = candidate
            return True
        self.__player = None
        return False

    def DrawPlayer(self, image, color=(0, 241, 255), thickness=2):
        if self.__player is None:
            return
        x, y, w, h = self.__player
        cv.rectangle(image, (x, y), (x + w, y + h), color, thickness)

    def DetectLevel(self, image):
        # TODO
        return True

    def DrawLevel(self, image, color=(255, 255, 255), thickness=2):
        if self.__level is None:
            return
        for lvl in self.__level:
            x, y, w, h = lvl
            cv.rectangle(image, (x, y), (x + w, y + h), color, thickness)

    def DetectMaskPoints(self, image, eps=10):
        objectRects = self.__DetectObjects(image)
        if objectRects is None:
            self.__maskPoints = None
            return False
        template = RemoveFloor(cv.imread('/data/maskpoints/maskpoints-1.png'))
        template = cv.cvtColor(template, cv.COLOR_BGR2GRAY)
        templateWidth, templateHeight = template.shape[::-1]
        gray = cv.cvtColor(RemoveFloor(image), cv.COLOR_BGR2GRAY)
        maskPoints = []
        for objectRect in objectRects:
            x, y, w, h = objectRect
            if w < templateWidth or h < templateHeight:
                continue
            if w > templateWidth + eps or h > templateHeight + eps:
                continue
            roi = gray[y:(y + h), x:(x + w)]
            matchingResults = cv.matchTemplate(roi, template, cv.TM_CCOEFF_NORMED)
            threshold = 0.8
            loc = np.where(matchingResults >= threshold)
            if len(loc[0]) > 0:
                maskPoints.append(objectRect)
        self.__maskPoints = maskPoints
        return True

    def DrawMaskPoints(self, image, color=(255, 255, 255), thickness=2):
        if self.__maskPoints is None:
            return
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

    def __DetectObjects(self, image, eps=10, minW=20, minH=30):
        contours = GetContours(image)
        if len(contours) == 0:
            return None
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
            return None
        objectRects = CreateRectGroups(rects=boundRectPass, minW=minW, minH=minH)
        return objectRects
