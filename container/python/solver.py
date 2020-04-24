#!/usr/bin/python
# -*- coding: utf-8 -*-

from .x11manager import X11Manager
from .detector import DetectGameRect
from .detector import DetectStartButtonRect
from .mitsudesu import Mitsudesu

def Main():
    x11 = X11Manager()
    gameRect = x11.Wait(stopFn=Detector.DetectGameRect)
    startButtonRect = x11.Wait(stopFn=Detector.DetectStartButtonRect)

    Mitsudesu
    x11.Click()

    gameRect = WaitDetection(window, DetectGameRect)
    startButtonRect = WaitDetection(window, DetectStartButtonRect, gameRect=gameRect)
    ClickStartButton(display, startButtonRect)
    RepeatSocialDistance(display, gameRect)

def WaitDetection(window, detectionFn, gameRect=None):
    res = None
    while res is None:
        sleep(0.5)
        image = GetImage(window)
        res = detectionFn(image, gameRect)
    return res

def ClickStartButton(display, startButtonRect):
    x = startButtonRect[0] + startButtonRect[2] / 2.0
    y = startButtonRect[1] + startButtonRect[3] / 2.0
    Click(display, x, y)

def RepeatSocialDistance(display, gameRect):
    x = gameRect[0] + gameRect[2] / 2.0
    y = gameRect[1] + gameRect[3] / 2.0
    while True:
        Click(display, x, y)

if __name__ == '__main__':
    Main()
