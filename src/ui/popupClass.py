import pygame as pg

from src.units.spriteClass import *

class Popup(Sprite):
    
    def __init__(self, gameObj, name, type, position, size, animation, sprite_id, priority, group):
        
        self.sprite_table = {"name": name, "type": type, "position": {"x": position.x, "y": position.y}, "size": {"width": size[0], "height": size[1]}, 
                             "sheets_path": animation, "id": sprite_id, "priority": priority, "obj_name": type + " " + str(len(group))}
        
        super().__init__(gameObj, self.sprite_table, group)
        
    def update(self):
        super().update()