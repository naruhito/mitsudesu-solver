# -*- coding: utf-8 -*-

from .utils import GetContours
from .utils import GetContourProperties
from .utils import CreateRectGroups

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
        objectRects = self.__DetectObjects(image)
        if objectRects is None:
            self.__maskPoints = None
            return False
        winSize = (20,20)
        blockSize = (10,10)
        blockStride = (5,5)
        cellSize = (10,10)
        nbins = 9
        derivAperture = 1
        winSigma = -1.
        histogramNormType = 0
        L2HysThreshold = 0.2
        gammaCorrection = 1
        nlevels = 64
        useSignedGradients = True
        hog = cv.HOGDescriptor(winSize,blockSize,blockStride,cellSize,nbins,derivAperture,winSigma,histogramNormType,L2HysThreshold,gammaCorrection,nlevels, useSignedGradients)

        data = []
        descriptors = []
        from .utils import RemoveFloor
        data.append(RemoveFloor(cv.imread('/data/maskpoints/maskpoints-2.png')))
        data.append(RemoveFloor(cv.imread('/data/maskpoints/maskpoints-1.png')))
        data.append(RemoveFloor(cv.imread('/data/level/l.png')))
        data.append(RemoveFloor(cv.imread('/data/level/1.png')))
        data.append(RemoveFloor(cv.imread('/data/level/v.png')))
        data.append(RemoveFloor(cv.imread('/data/level/e.png')))
        data.append(RemoveFloor(cv.imread('/data/player/player-3.png')))
        data.append(RemoveFloor(cv.imread('/data/player/player-1.png')))
        data.append(RemoveFloor(cv.imread('/data/player/player-2.png')))
        data.append(RemoveFloor(cv.imread('/data/enemies/enemies-3.png')))
        data.append(RemoveFloor(cv.imread('/data/enemies/enemies-2.png')))
        data.append(RemoveFloor(cv.imread('/data/enemies/enemies-1.png')))
        for img in data:
            img2 = cv.resize(img, (64, 128))
            descriptors.append(hog.compute(img2))
        # import IPython; IPython.embed()

        import numpy as np

        # data2 = []
        # for img in data:
        #     hoge = img.reshape(img.shape[0] * img.shape[1] * 3)
        #     data2.append(hoge)
        # data = np.array(data2, np.float32)

        svm = cv.ml.SVM_create()
        svm.setType(cv.ml.SVM_C_SVC)
        svm.setKernel(cv.ml.SVM_RBF)
        svm.setC(12.5)
        svm.setGamma(0.50625)

        positive_images = descriptors[:2]
        negative_images = descriptors[2:]
        images = np.r_[positive_images, negative_images]

        positive_labels = np.ones(len(data[:2]), np.int32)
        negative_labels = np.zeros(len(data[2:]), np.int32)
        labels = np.array([np.r_[positive_labels, negative_labels]])

        # import IPython; IPython.embed()
        svm.train(images, cv.ml.ROW_SAMPLE, labels)

        testResponse = svm.predict(images)
        # import IPython; IPython.embed()

        resres = []
        for i, objectRect in enumerate(objectRects):
            x, y, w, h = objectRect
            roi = RemoveFloor(image[y:y+h, x:x+w])
            roi = cv.resize(roi, (64, 128))
            des = hog.compute(roi)
            # svm.predict(np.r_[[des]])
            # import IPython; IPython.embed()
            bbb = svm.predict(np.r_[[des]])
            cv.imwrite('/image/{}.png'.format(i), roi)
            if int(bbb[1][0][0]) == 1:
                resres.append(objectRect)


        img_rgb = image
        
        template = cv.imread('data/player/player-1.png', 0)
        # template = cv.imread('data/enemies/enemies-2.png', 0)
        
        import numpy as np
        
        img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
        
        
        w, h = template.shape[::-1]
        
        res = cv.matchTemplate(img_gray,template,cv.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where( res >= threshold)
        resres2 = []
        for pt in zip(*loc[::-1]):
            x, y, w, h = pt[0], pt[1], w, h
            resres2.append((x, y, w, h))

        self.__maskPoints = resres2
        return True

    def DrawMaskPoints(self, image, color=(0, 241, 255), thickness=2):
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
