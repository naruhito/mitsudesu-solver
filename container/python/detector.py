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
            self.__gameRect = None
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
            self.__gameRect = None
            return False
        self.__gameRect = boundRectPass[0]
        return True

    def DrawGameRect(self, image, color=(0, 241, 255), thickness=2):
        x, y, w, h = self.__gameRect
        cv.rectangle(image, (x, y), (x + w, y + h), color, thickness)

    def DetectStartButtonNormalRect(self, image, width=114, height=53, eps=10):
        contours = self.__GetContours(image)
        if len(contours) == 0:
            self.__startButtonNormalRect = None
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
        contours = self.__GetContours(image)
        if len(contours) == 0:
            self.__maskPoints = None
            return False
        centerList, arcLengthList, boundRectList = self.__GetContourProperties(contours)
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
        self.__maskPoints = self.__RectsFilter(rects=boundRectPass, minW=20, minH=30)
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

    def __RectsFilter(self, rects, minW, minH):
        res = []
        while len(rects) > 0:
            rect = rects.pop(0)
            while True:
                changed = False
                rectsUnused = []
                for rect2 in rects:
                    if not self.__RectIsIntersected(rect, rect2):
                        rectsUnused.append(rect2)
                        continue
                    if rect[2] > minW and rect[3] > minH:
                        res.append(rect)
                    if rect2[2] > minW and rect2[3] > minH:
                        res.append(rect2)
                    rect = self.__RectUnite(rect, rect2)
                    changed = True
                rects = rectsUnused
                if not changed:
                    break
            res.append(rect)
        return res

    def __RectIsIntersected(self, a, b):
        x = max(a[0], b[0])
        y = max(a[1], b[1])
        w = min(a[0] + a[2], b[0] + b[2]) - x
        h = min(a[1] + a[3], b[1] + b[3]) - y
        if w < 0 or h < 0:
            return False
        return True

    def __RectUnite(self, a, b):
        x = min(a[0], b[0])
        y = min(a[1], b[1])
        w = max(a[0] + a[2], b[0] + b[2]) - x
        h = max(a[1] + a[3], b[1] + b[3]) - y
        return x, y, w, h
