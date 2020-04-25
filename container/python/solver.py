#!/usr/bin/python
# -*- coding: utf-8 -*-

from .x11manager import X11Manager
from .detector import Detector
from .planner import Planner

def Main():
    x11 = X11Manager()
    detector = Detector()
    planner = Planner()

    x11.Wait(breakFn=detector.DetectGameRect)
    x11.Wait(breakFn=detector.DetectStartButtonNormalRect)
    startButtonNormalRect = detector.GetStartButtonNormalRect()
    startNormalAction = planner.PlanStartNormalAction(startButtonNormalRect)
    x11.ProcessActoin(action=startNormalAction)

    while True:
        x11.Wait(breakFn=detector.DetectPlayer)
        x11.Wait(breakFn=detector.DetectLevel)
        x11.Wait(breakFn=detector.DetectMaskPoints)
        x11.Wait(breakFn=detector.DetectSocialDistance)
        x11.Wait(breakFn=detector.DetectEnemies)
        x11.Wait(breakFn=detector.DetectAvesans)
        x11.Wait(breakFn=detector.DetectItems)
        gameRect = detector.GetGameRect()
        player = detector.GetPlayer()
        level = detector.GetLevel()
        maskPoints = detector.GetMaskPoints()
        socialDistance = detector.GetSocialDistance()
        enemies = detector.GetEnemies()
        avesans = detector.GetAvesans()
        items = detector.GetItems()
        socialDistanceAction = planner.PlanSocialDistanceAction(
            gameRect=gameRect,
            player=player,
            level=level,
            maskPoints=maskPoints,
            socialDistance=socialDistance,
            enemies=enemies,
            avesans=avesans,
            items=items,
        )
        x11.ProcessActoin(action=socialDistanceAction)

if __name__ == '__main__':
    Main()
