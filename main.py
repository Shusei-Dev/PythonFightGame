import pygame as pg
import sys

from src.misc.settingsClass import *
from src.misc.window import *
from src.misc.inputs import *
from src.misc.debug import *
from src.assets.assets import *
from src.world.world import *
from src.misc.layer import LayerManager


class GameEngine:
    
    def __init__(self):
        self.settings = Settings(self)
        self.window = Window(self, self.settings.data["display"]["size"], self.settings.data["name"], self.settings.data["version"], self.settings.data["display"]["framerate"])
        self.inputs = Inputs(self)
        self.debug = Debug(self)

        self.layer_manager = LayerManager()
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
    GameEngine().run()