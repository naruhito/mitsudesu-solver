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

    def __init__(self, display, width, height):
        self.__xdisplay = Display(display)
        self.__window = self.__xdisplay.screen().root
        self.__width = width
        self.__height = height

    def Wait(self, breakFn):
        while True:
            image = self.__GetImage()
            if breakFn(image=image):
                return image
            sleep(0.5)

    def ProcessActoin(self, action):
        x = action[0]
        y = action[1]
        duration = action[2]
        fake_input(self.__xdisplay, MotionNotify, x=x, y=y)
        fake_input(self.__xdisplay, ButtonPress, 1)
        self.__xdisplay.sync()
        sleep(duration)
        fake_input(self.__xdisplay, ButtonRelease, 1)
        self.__xdisplay.sync()

    def __GetImage(self):
        rawImage = self.__window.get_image(0, 0, self.__width, self.__height, ZPixmap, 0xFFFFFFFF).data
        pilImage = Image.frombytes('RGB', (self.__width, self.__height), rawImage, 'raw', 'RGBX')
        return asarray(pilImage)
