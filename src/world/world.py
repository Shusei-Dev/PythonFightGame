import pygame as pg

from src.ui.guiManager import *
from src.units.entityManager import *


class World():

    def __init__(self, gameObj):
        self.gameObj = gameObj

        self.guiManager = GuiManager(self.gameObj)
        self.entityManager = EntityManager(self.gameObj)
        # TODO: add the game state system
        self.game_state = "Menu"


    def update(self):
        # Update the gui manager
        self.guiManager.update()
        self.entityManager.update()
        #print(self.gameObj.window.all_sprite.sprites()[0].position)
        

    def render(self):
        # Render all sprite on the display surface
        
        for sprites in self.gameObj.layer_manager.draw_layers():
            
            self.gameObj.window.display.blit(sprites[0], sprites[1])

    #def load_world(self)