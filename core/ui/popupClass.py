import pygame as pg

from core.units.spriteClass import *

class Popup(Sprite):
    
    def __init__(self, gameObj, name, type, position, size, animation, sprite_id, priority, group):
        super().__init__(gameObj, name, type, position, size, animation, sprite_id, priority, group, gameObj.window.all_sprite)
        
    def update(self):
        super().update()