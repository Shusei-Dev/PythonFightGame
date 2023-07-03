import pygame as pg

from core.ui.guiManager import *
from core.units.entityManager import *

class World():

    def __init__(self, gameObj):
        self.gameObj = gameObj

        self.guiManager = guiManager(self.gameObj)
        self.entityManager = entityManager(self.gameObj)
        # TODO: add the game state system
        self.game_state = "Menu"


    def update(self):
        # Update the gui manager
        self.guiManager.update()
        self.entityManager.update()
        #print(self.gameObj.window.all_sprite.sprites()[0].position)
        

    def render(self):
        # Render all sprite on the display surface
        self.gameObj.window.all_sprite.draw(self.gameObj.window.display)
