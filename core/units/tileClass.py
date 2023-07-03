import pygame as pg

from core.units.spriteClass import *
from core.misc.spr_sheet_loader import *

class Tile(Sprite):
    
    def __init__(self, gameObj, sprite_table, groups):
        self.gameObj = gameObj
        self.table = sprite_table[0]
        
        name = sprite_table[1]
        position = pg.Vector2(0, 0)
        size = (self.table["size"]["width"], self.table["size"]["height"])
        
        self.priority = int(self.table["priority"])
        self.tile_name = self.table["name"]
        self.sprite_id = self.table["id"]
        
        if isinstance(self.table["sheets"], dict):
            sheets_name = self.table["sheets"].keys()
            self.sheets = {}
            
            for sheets in sheets_name:
                self.sheets[sheets] = load_sheet(self.table["sheets"][sheets]["path"], self.table["sheets"][sheets]["size"]["width"], self.table["sheets"][sheets]["size"]["height"], self.table["sheets"][sheets]["spr_number"])
        else:
            self.sheets = self.table["image_path"]
        
        super().__init__(gameObj, name, type, position, size, self.sheets, self.sprite_id, self.priority, groups[0], self.gameObj.window.all_sprite)
