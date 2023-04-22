import pygame as pg
import sys

from core.misc.settingsClass import *
from core.misc.window import *
from core.misc.inputs import *
from core.misc.debug import *
from core.assets.assets import *
from core.world.world import *

class FightGame:

    def __init__(self):
        self.settings = Settings(self)
        self.window = Window(self, self.settings.data["display"]["size"], self.settings.data["name"], self.settings.data["version"], self.settings.data["display"]["framerate"])
        self.inputs = Inputs(self)
        self.debug = Debug(self)

        self.assets = Assets(self)

        self.world = World(self)


    def update(self):
        self.inputs.update()
        self.world.update()
        self.world.render()
        self.window.update()

    def quit(self):
        self.window.running = False
        pg.quit()
        sys.exit()

    def run(self):
        while self.window.running:
            self.update()


if __name__ == '__main__':
    FightGame().run()
