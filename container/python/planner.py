# -*- coding: utf-8 -*-

from .utils import GetRectCenter

class Planner(object):

    def __init__(self):
        pass

    def PlanStartNormalAction(self, startButtonNormalRect):
        x = startButtonNormalRect[0] + startButtonNormalRect[2] / 2.0
        y = startButtonNormalRect[1] + startButtonNormalRect[3] / 2.0
        return x, y, 1.0

    def PlanSocialDistanceAction(self, gameRect, player, level, maskPoints, socialDistance, enemies, avesans, items):
        if player is None:
            return self.__GetDefaultAction(gameRect)
        if enemies is None:
            return self.__GetDefaultAction(gameRect)
        return self.__GetDefaultAction(gameRect)

    def __GetDefaultAction(self, gameRect):
        x = gameRect[0] + gameRect[2] / 2.0
        y = gameRect[1] + gameRect[3] / 2.0
        duration = 1.0
        return x, y, duration

    def __GetClosestEnemy(self, player, enemies):
        pass
