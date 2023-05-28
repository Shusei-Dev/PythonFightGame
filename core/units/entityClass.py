import pygame as pg

from core.units.spriteClass import *
from core.misc.spr_sheet_loader import *

class Entity(Sprite):
    
    def __init__(self, gameObj, sprite_table, groups):
        self.gameObj = gameObj
        self.table = sprite_table[0]
        
        name = sprite_table[1]
        position = pg.Vector2(self.table["position"]["x"], self.table["position"]["y"])
        size = (self.table["size"]["width"], self.table["size"]["height"])
        
        self.priority = int(self.table["priority"])
        self.player_name = self.table["name"]
        
        
        if isinstance(self.table["sheets"], dict):
            sheets_name = self.table["sheets"].keys()
            self.sheets = {}
            
            for sheets in sheets_name:
                self.sheets[sheets] = load_sheet(self.table["sheets"][sheets]["path"], self.table["sheets"][sheets]["size"]["width"], self.table["sheets"][sheets]["size"]["height"], self.table["sheets"][sheets]["spr_number"])
        
        self.sprite_id = self.table["id"]
        
        self.base_health = self.table["health"]
        self.health = self.table["health"]
        self.velocity = self.table["velocity"]
        
        super().__init__(gameObj, name, "entity", position, size, self.sheets, self.sprite_id, self.priority, groups[0], self.gameObj.window.all_sprite)
        
        
    def update(self):
        super().update()
        
        
        self.set_animation("right", [0.4, 0.4])
        #self.position.x += 0.2