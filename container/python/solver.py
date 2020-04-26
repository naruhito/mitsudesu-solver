#!/usr/bin/python
# -*- coding: utf-8 -*-

from .x11manager import X11Manager
from .detector import Detector
from .planner import Planner

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
        image = self.__x11.GetImage()
        self.__detector.DetectLevel(image)
        self.__detector.DetectMaskPoints(image)
        self.__detector.DetectSocialDistance(image)
        self.__detector.DetectEnemies(image)
        self.__detector.DetectAvesans(image)
        self.__detector.DetectItems(image)
        socialDistanceAction = self.__planner.PlanSocialDistanceAction(
            gameRect=self.__detector.GetGameRect(),
            player=self.__detector.GetPlayer(),
            level=self.__detector.GetLevel(),
            maskPoints=self.__detector.GetMaskPoints(),
            socialDistance=self.__detector.GetSocialDistance(),
            enemies=self.__detector.GetEnemies(),
            avesans=self.__detector.GetAvesans(),
            items=self.__detector.GetItems(),
        )
        self.__x11.ProcessActoin(action=socialDistanceAction)
        self.__detector.DrawGameRect(image)
        self.__detector.DrawLevel(image)
        self.__detector.DrawMaskPoints(image)
        self.__detector.DrawSocialDistance(image)
        self.__detector.DrawEnemies(image)
        self.__detector.DrawAvesans(image)
        self.__detector.DrawItems(image)
        self.__ShowDebugImage(image)

    def __ShowDebugImage(self, image, duration=1):
        _display = environ.get('DISPLAY', '')
        environ['DISPLAY'] = self.__displayDebug
        imshow('detection results', image)
        waitKey(duration)
        environ['DISPLAY'] = _display

if __name__ == '__main__':
    Main()
