# -*- coding: utf-8 -*-

from .utils import GetRectCenter
from .utils import GetRectDistance

class Planner(object):

    def __init__(self):
        self.__socialDistanceRadius = None

    def PlanStartNormalAction(self, startButtonNormalRect):
        x, y = GetRectCenter(startButtonNormalRect)
        return x, y, 1.0

    def PlanSocialDistanceAction(self, gameRect, player, level, maskPoints, socialDistance, enemies, avesans, items, eps=10):
        if socialDistance is not None:
            self.__UpdateSocialDistanceRadius(socialDistance)
        if player is None:
            return self.__GetDefaultAction(gameRect)
        if enemies is None or len(enemies) == 0:
            return self.__GetDefaultAction(gameRect)
        closestEnemy = self.__GetClosestEnemy(player, enemies)
        if closestEnemy is None:
            return self.__GetDefaultAction(gameRect)
        x, y = GetRectCenter(closestEnemy)
        return x, y - eps, 1.0

    def __GetDefaultAction(self, gameRect):
        x, y = GetRectCenter(gameRect)
        return x, y, 1.0

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
                if enemy[1] < player[0] + player[2]:
                    continue
            closestEnemy = enemy
            break
        return closestEnemy
