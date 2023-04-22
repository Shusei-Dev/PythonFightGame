import pygame as pg
from pygame.locals import *


class Inputs():

    def __init__(self, gameObj):
        self.gameObj = gameObj

        self.mouse_event = MouseEventHandler()


    def update(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.gameObj.quit()
                
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.gameObj.quit()


        self.mouse_event.btn_pressed(pg.mouse.get_pressed())

        #print(self.mouse_event.LEFT_CLICK)


class MouseEventHandler():
    def __init__(self):
        self.mouse = []
        self.LEFT_CLICK = [False, 0]
        self.RIGHT_CLICK = [False, 0]
        self.MIDDLE_CLICK = [False, 0]
        self.POS = (0, 0)

    def btn_pressed(self, mouseObj):
        self.mouse = mouseObj
        self.POS = pg.mouse.get_pos()

        self.LEFT_CLICK[0] = self.mouse[0]
        self.RIGHT_CLICK[0] = self.mouse[2]
        self.MIDDLE_CLICK[0] = self.mouse[1]

        if self.LEFT_CLICK[0]:
            self.LEFT_CLICK[1] += 1
        else:
            self.LEFT_CLICK[1] = 0

        if self.RIGHT_CLICK[0]:
            self.RIGHT_CLICK[1] += 1
        else:
            self.RIGHT_CLICK[1] = 0

        if self.MIDDLE_CLICK[0]:
            self.MIDDLE_CLICK[1] += 1
        else:
            self.MIDDLE_CLICK[1] = 0
