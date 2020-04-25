# -*- coding: utf-8 -*-

from Xlib.display import Display
from Xlib.X import ZPixmap
from Xlib.X import MotionNotify
from Xlib.X import ButtonPress
from Xlib.X import ButtonRelease
from Xlib.ext.xtest import fake_input
from PIL import Image
from time import sleep
from numpy import asarray

class X11Manager(object):

    def __init__(self, w=1024, h=768):
        self.__w = w
        self.__h = h
        self.__display = Display()
        self.__window = self.__display.screen().root

    def Wait(self, breakFn):
        while True:
            image = self.__GetImage()
            if breakFn(image=image):
                break
            sleep(0.5)

    def ProcessActoin(self, action):
        x = int(action[0])
        y = int(action[1])
        duration = action[2]
        fake_input(self.__display, MotionNotify, x=x, y=y)
        fake_input(self.__display, ButtonPress, 1)
        self.__display.sync()
        sleep(duration)
        fake_input(self.__display, ButtonRelease, 1)
        self.__display.sync()

    def __GetImage(self):
        rawImage = self.__window.get_image(0, 0, self.__w, self.__h, ZPixmap, 0xFFFFFFFF).data
        pilImage = Image.frombytes('RGB', (self.__w, self.__h), rawImage, 'raw', 'RGBX')
        return asarray(pilImage)
