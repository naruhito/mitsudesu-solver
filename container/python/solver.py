#!/usr/bin/python
# -*- coding: utf-8 -*-

from .x11manager import X11Manager
from .detector import Detector
from .planner import Planner
from .utils import RemoveFloor

from argparse import ArgumentParser
from os import environ
from cv2 import imshow
from cv2 import waitKey

def Main():
    parser = ArgumentParser(description='Simple solver of "Mitsu-desu" game.')
    parser.add_argument('--display-width', type=int, required=True)
    parser.add_argument('--display-height', type=int, required=True)
    parser.add_argument('--display-x11', type=str, required=True)
    parser.add_argument('--display-debug', type=str, required=True)
    args = parser.parse_args()
    solver = Solver(width=args.display_width,
                    height=args.display_height,
                    displayX11=args.display_x11,
                    displayDebug=args.display_debug)
    solver.SolveStartButtonNormal()
    while True:
        solver.SolveSocialDistance()

class Solver(object):

    def __init__(self, width, height, displayX11, displayDebug):
        self.__x11 = X11Manager(display=displayX11, width=width, height=height)
        self.__detector = Detector()
        self.__planner = Planner()
        self.__displayDebug = displayDebug

    def SolveStartButtonNormal(self):
        self.__x11.Wait(breakFn=self.__detector.DetectGameRect)
        self.__x11.Wait(breakFn=self.__detector.DetectStartButtonNormalRect)
        startButtonNormalRect = self.__detector.GetStartButtonNormalRect()
        startNormalAction = self.__planner.PlanStartNormalAction(startButtonNormalRect=startButtonNormalRect)
        self.__x11.ProcessActoin(action=startNormalAction)

    def SolveSocialDistance(self):
        image = self.__x11.Wait(breakFn=self.__detector.DetectGameObjects)
        player, level, maskPoints, socialDistance, enemies, avesans, items = self.__detector.GetGameObjects()
        socialDistanceAction = self.__planner.PlanSocialDistanceAction(
            player=player,
            level=level,
            maskPoints=maskPoints,
            socialDistance=socialDistance,
            enemies=enemies,
            avesans=avesans,
            items=items,
        )
        if socialDistanceAction is not None:
            self.__x11.ProcessActoin(action=socialDistanceAction)
            self.__planner.DrawSocialDistanceAction(image)
        self.__detector.DrawGameRect(image)
        self.__detector.DrawGameObjects(image)
        self.__ShowDebugImage(image)

    def __ShowDebugImage(self, image, duration=1):
        _display = environ.get('DISPLAY', '')
        environ['DISPLAY'] = self.__displayDebug
        imshow('debug', RemoveFloor(image))
        waitKey(duration)
        environ['DISPLAY'] = _display

if __name__ == '__main__':
    Main()
