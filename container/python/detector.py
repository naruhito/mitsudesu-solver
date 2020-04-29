# -*- coding: utf-8 -*-

from .utils import GetContours
from .utils import GetContourProperties
from .utils import CreateRectGroups
from .utils import RemoveFloor
from .utils import RemoveSocialDistance
from .utils import GetTrainedSvm
from .utils import GetHogDescriptor
from .utils import ResizeHog

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
        self.__svm = GetTrainedSvm()
        self.__hog = GetHogDescriptor()

    def GetGameRect(self):
        return self.__gameRect

    def GetStartButtonNormalRect(self):
        return self.__startButtonNormalRect

    def GetGameObjects(self):
        return self.__player, self.__level, self.__maskPoints, self.__socialDistance, self.__enemies, self.__avesans, self.__items

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

    def DetectGameObjects(self, image):
        contourRects = self.__DetectContourRects(image)
        if len(contourRects) == 0:
            self.__ClearGameObjects()
            return False
        descriptors = []
        for contourRect in contourRects:
            x, y, w, h = contourRect
            roi = RemoveFloor(image[y:(y + h), x:(x + w)])
            roi = RemoveSocialDistance(roi)
            resized = ResizeHog(roi)
            des = self.__hog.compute(resized)
            descriptors.append(des)
        predictions = self.__svm[0].predict(np.array(descriptors))[1]
        dataTypes = self.__svm[1]
        predictedDataTypes = []
        for prediction in predictions:
            dataType = dataTypes[int(prediction[0])]
            predictedDataTypes.append(dataType)
        self.__ClearGameObjects()
        self.__DetectPlayer(image, contourRects, predictedDataTypes)
        self.__DetectLevel(image, contourRects, predictedDataTypes)
        self.__DetectMaskPoints(image, contourRects, predictedDataTypes)
        self.__DetectSocialDistance(image, contourRects, predictedDataTypes)
        self.__DetectEnemies(image, contourRects, predictedDataTypes)
        self.__DetectAvesans(image, contourRects, predictedDataTypes)
        self.__DetectItems(image, contourRects, predictedDataTypes)
        return True

    def DrawGameRect(self, image, color=(0, 241, 255), thickness=2):
        x, y, w, h = self.__gameRect
        cv.rectangle(image, (x, y), (x + w, y + h), color, thickness)

    def DrawStartButtonNormalRect(self, image, color=(0, 241, 255), thickness=2):
        x, y, w, h = self.__startButtonNormalRect
        cv.rectangle(image, (x, y), (x + w, y + h), color, thickness)

    def DrawGameObjects(self, image):
        self.__DrawPlayer(image)
        self.__DrawLevel(image)
        self.__DrawMaskPoints(image)
        self.__DrawSocialDistance(image)
        self.__DrawEnemies(image)
        self.__DrawAvesans(image)
        self.__DrawItems(image)

    def __DetectContourRects(self, image, eps=10, minW=20, minH=30):
        contours = GetContours(image)
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
        contourRects = CreateRectGroups(rects=boundRectPass, minW=minW, minH=minH)
        return contourRects

    def __ClearGameObjects(self):
        self.__player = None
        self.__level = None
        self.__maskPoints = None
        self.__socialDistance = None
        self.__enemies = None
        self.__avesans = None
        self.__items = None

    def __DetectPlayer(self, image, contourRects, predictedDataTypes):
        candidates = []
        for gameObjectRect, predictedDataType in zip(contourRects, predictedDataTypes):
            if predictedDataType == 'player':
                candidates.append(gameObjectRect)
        if len(candidates) == 0:
            return
        self.__player = candidates[0]

    def __DetectLevel(self, image, contourRects, predictedDataTypes, eps=10, threshold=0.8):
        # TODO
        candidates = []
        for gameObjectRect, predictedDataType in zip(contourRects, predictedDataTypes):
            if predictedDataType == 'level':
                candidates.append(gameObjectRect)
        self.__level = candidates
        # template = RemoveFloor(cv.imread('/data/maskpoints/maskpoints-1.png'))  # try using template matching instead of SVM
        # template = cv.cvtColor(template, cv.COLOR_BGR2GRAY)
        # templateWidth, templateHeight = template.shape[::-1]
        # gray = cv.cvtColor(RemoveFloor(image), cv.COLOR_BGR2GRAY)
        # maskPoints = []
        # for contourRect in contourRects:
        #     x, y, w, h = contourRect
        #     if w < templateWidth or h < templateHeight:
        #         continue
        #     if w > templateWidth + eps or h > templateHeight + eps:
        #         continue
        #     roi = gray[y:(y + h), x:(x + w)]
        #     matchingResults = cv.matchTemplate(roi, template, cv.TM_CCOEFF_NORMED)
        #     loc = np.where(matchingResults >= threshold)
        #     if len(loc[0]) > 0:
        #         maskPoints.append(contourRect)
        # self.__maskPoints = maskPoints

    def __DetectMaskPoints(self, image, contourRects, predictedDataTypes):
        candidates = []
        for gameObjectRect, predictedDataType in zip(contourRects, predictedDataTypes):
            if predictedDataType == 'maskpoints':
                candidates.append(gameObjectRect)
        self.__maskPoints = candidates

    def __DetectSocialDistance(self, image, contourRects, predictedDataTypes):
        # TODO
        pass

    def __DetectEnemies(self, image, contourRects, predictedDataTypes):
        candidates = []
        for gameObjectRect, predictedDataType in zip(contourRects, predictedDataTypes):
            if predictedDataType == 'enemies':
                candidates.append(gameObjectRect)
        if len(candidates) == 0:
            return
        self.__enemies = candidates

    def __DetectAvesans(self, image, contourRects, predictedDataTypes):
        # TODO
        pass

    def __DetectItems(self, image, contourRects, predictedDataTypes):
        # TODO
        pass

    def __DrawPlayer(self, image, color=(0, 241, 255), thickness=2):
        if self.__player is None:
            return
        x, y, w, h = self.__player
        cv.rectangle(image, (x, y), (x + w, y + h), color, thickness)

    def __DrawLevel(self, image, color=(255, 0, 0), thickness=2):
        if self.__level is None:
            return
        for lvl in self.__level:
            x, y, w, h = lvl
            cv.rectangle(image, (x, y), (x + w, y + h), color, thickness)

    def __DrawMaskPoints(self, image, color=(255, 255, 255), thickness=2):
        if self.__maskPoints is None:
            return
        for maskPoint in self.__maskPoints:
            x, y, w, h = maskPoint
            cv.rectangle(image, (x, y), (x + w, y + h), color, thickness)

    def __DrawSocialDistance(self, image):
        # TODO
        pass

    def __DrawEnemies(self, image, color=(0, 0, 255), thickness=2):
        if self.__enemies is None:
            return
        for enemy in self.__enemies:
            x, y, w, h = enemy
            cv.rectangle(image, (x, y), (x + w, y + h), color, thickness)

    def __DrawAvesans(self, image):
        # TODO
        pass

    def __DrawItems(self, image):
        # TODO
        pass
