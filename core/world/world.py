import pygame as pg

from core.ui.guiManager import *

class World():

    def __init__(self, gameObj):
        self.gameObj = gameObj

        self.guiManager = guiManager(self.gameObj)
        self.game_state = "Menu"


    def update(self):
        # Update the gui manager
        self.guiManager.update()
        #print(self.gameObj.window.all_sprite.sprites()[0].position)
        

    def render(self):
        # Render all gui
        self.gameObj.window.all_sprite.draw(self.gameObj.window.display)
