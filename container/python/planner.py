# -*- coding: utf-8 -*-

from .utils import GetRectCenter
from .utils import GetRectDistance

import cv2 as cv
import numpy as np

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
        x, y, duration = self.__socialDistanceAction
        r = int(self.__GetSocialDistanceRadius() * duration)
        cv.circle(image, (x, y), r, color, thickness)

    def PlanSocialDistanceAction(self, player, levels, maskPoints, socialDistance, enemies, avesans, items, duration=0.3, eps=10):
        self.__socialDistanceAction = None
        if socialDistance is not None:
            self.__socialDistance = socialDistance
        if player is not None:
            self.__player = player
        closestEnemy = self.__GetClosestEnemy(enemies)
        if closestEnemy is None:
            return None
        cPlayer = np.array(GetRectCenter(self.__player))
        cEnemy = np.array(GetRectCenter(closestEnemy))
        v = cEnemy - cPlayer
        d = np.linalg.norm(v)
        dd = GetRectDistance(self.__player, closestEnemy)
        actionXY = cPlayer + v * dd / d
        if abs(actionXY[0] - closestEnemy[0]) < eps:
            if actionXY[0] > closestEnemy[0]:
                actionXY[0] += eps
            else:
                actionXY[0] -= eps
        self.__socialDistanceAction = int(actionXY[0]), int(actionXY[1]), duration
        return self.__socialDistanceAction

    def __GetSocialDistanceRadius(self):
        if self.__socialDistance is None:
            return None
        return self.__socialDistance[2] / 2.0

    def __GetClosestEnemy(self, enemies, eps=10, maxEnemyW=100, maxEnemyH=100):
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
            if distance + eps < socialDistanceRadius:
                continue
            if enemy[1] > self.__player[1]:
                continue
            if enemy[2] > maxEnemyW:
                continue
            if enemy[3] > maxEnemyH:
                continue
            closestEnemy = enemy
            break
        return closestEnemy
