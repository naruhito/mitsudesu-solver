# -*- coding: utf-8 -*-

from .utils import GetRectCenter
from .utils import GetRectDistance

import cv2 as cv

class Planner(object):

    def __init__(self):
        self.__socialDistanceRadius = None
        self.__action = None

    def GetAction(self):
        return self.__action

    def DrawAction(self, image, color=(0, 241, 255), thickness=5):
        x, y, _ = self.__action
        if self.__socialDistanceRadius is None:
            return
        r = int(self.__socialDistanceRadius)
        cv.circle(image, (x, y), r, color, thickness)

    def PlanStartNormalAction(self, startButtonNormalRect):
        x, y = GetRectCenter(startButtonNormalRect)
        self.__action = (int(x), int(y), 1.0)

    def PlanSocialDistanceAction(self, gameRect, player, level, maskPoints, socialDistance, enemies, avesans, items):
        if socialDistance is not None:
            self.__UpdateSocialDistanceRadius(socialDistance)
        if player is None:
            self.__action = None
            return
        if enemies is None or len(enemies) == 0:
            self.__action = None
            return
        closestEnemy = self.__GetClosestEnemy(player, enemies)
        if closestEnemy is None:
            self.__action = None
            return
        x, y = GetRectCenter(closestEnemy)
        r = self.__socialDistanceRadius or 50
        self.__action = int(x), int(y + r), 1.0

    def __UpdateSocialDistanceRadius(self, socialDistance, eps=10):
        x, y, w, h = socialDistance
        r = w / 2.0
        if self.__socialDistanceRadius is None:
            self.__socialDistanceRadius = r
            return
        if abs(self.__socialDistanceRadius - r) < eps:
            return
        self.__socialDistanceRadius = r

    def __GetClosestEnemy(self, player, enemies):
        distances = []
        for enemy in enemies:
            distance = GetRectDistance(player, enemy)
            distances.append(distance)
        closestEnemy = None
        for distance, enemy in sorted(zip(distances, enemies), key=lambda x: x[0]):
            if self.__socialDistanceRadius is not None:
                if distance < self.__socialDistanceRadius:
                    continue
            if enemy[1] + enemy[3] > player[1]:
                continue
            closestEnemy = enemy
            break
        return closestEnemy
