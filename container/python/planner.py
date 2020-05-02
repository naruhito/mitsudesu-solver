# -*- coding: utf-8 -*-

from .utils import GetRectCenter
from .utils import GetRectDistance

import cv2 as cv

class Planner(object):

    def __init__(self):
        self.__socialDistance = None
        self.__player = None
        self.__socialDistanceAction = None

    def PlanStartNormalAction(self, startButtonNormalRect):
        x, y = GetRectCenter(startButtonNormalRect)
        return int(x), int(y), 1.0

    def DrawSocialDistanceAction(self, image, color=(0, 241, 255), thickness=5):
        if self.__socialDistanceAction is None:
            return
        x, y, _ = self.__socialDistanceAction
        r = int(self.__GetSocialDistanceRadius())
        cv.circle(image, (x, y), r, color, thickness)

    def PlanSocialDistanceAction(self, player, levels, maskPoints, socialDistance, enemies, avesans, items):
        self.__socialDistanceAction = None
        if socialDistance is not None:
            self.__socialDistance = socialDistance
        if player is not None:
            self.__player = player
        closestEnemy = self.__GetClosestEnemy(enemies)
        if closestEnemy is None:
            return None
        x, y = GetRectCenter(closestEnemy)  # FIXME
        r = self.__GetSocialDistanceRadius()  # FIXME
        self.__socialDistanceAction = int(x), int(y + r), 1.0  # FIXME
        return self.__socialDistanceAction

    def __GetSocialDistanceRadius(self):
        if self.__socialDistance is None:
            return None
        return self.__socialDistance[2] / 2.0

    def __GetClosestEnemy(self, enemies):
        if enemies is None:
            return None
        if self.__socialDistance is None:
            return None
        if self.__player is None:
            return None
        distances = []
        for enemy in enemies:
            distance = GetRectDistance(self.__player, enemy)
            distances.append(distance)
        socialDistanceRadius = self.__GetSocialDistanceRadius()
        closestEnemy = None
        for distance, enemy in sorted(zip(distances, enemies), key=lambda x: x[0]):
            if socialDistanceRadius is not None and distance < socialDistanceRadius:
                continue
            if enemy[1] + enemy[3] > self.__player[1]:
                continue
            closestEnemy = enemy
            break
        return closestEnemy
