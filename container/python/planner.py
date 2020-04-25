# -*- coding: utf-8 -*-

class Planner(object):

    def __init__(self):
        pass

    def PlanStartNormalAction(self, startButtonNormalRect):
        x = startButtonNormalRect[0] + startButtonNormalRect[2] / 2.0
        y = startButtonNormalRect[1] + startButtonNormalRect[3] / 2.0
        return x, y, 1.0

    def PlanSocialDistanceAction(self, gameRect, player, level, maskPoints, socialDistance, enemies, avesans, items):
        # TODO
        x = gameRect[0] + gameRect[2] / 2.0
        y = gameRect[1] + gameRect[3] / 2.0
        return x, y, 1.0
