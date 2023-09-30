import pygame as pg

from src.units.spriteClass import *
from src.misc.spr_sheet_loader import *

class Entity(Sprite):
    
    def __init__(self, gameObj, sprite_table, groups):
        self.gameObj = gameObj
        self.table = sprite_table[0]
        
        # Init the basics of a sprite unit
        
        self.priority = int(self.table["priority"])
        self.player_name = self.table["name"]
        
        if isinstance(self.table["sheets_path"], dict):
            sheets_name = self.table["sheets_path"].keys()
            self.sheets = {}
            
            for sheets in sheets_name:
                self.sheets[sheets] = load_sheet(self.table["sheets_path"][sheets]["path"], self.table["sheets_path"][sheets]["size"]["width"], self.table["sheets_path"][sheets]["size"]["height"], self.table["sheets_path"][sheets]["spr_number"])
        
        # Init all basics of an entity
        
        self.base_health = self.table["health"]
        self.old_hp = self.table["health"]
        self.health = self.table["health"]
        self.speed = self.table["speed"]
        
        self.vel_x = 0
        self.vel_y = 0
        
        self.directions = ["none", "forward", "backward", "left", "right"]
        self.direction = self.directions[0]
        self.old_direction = self.directions[0]
        self.action = None
        
        self.table["obj_name"] = sprite_table[1]
        self.table["sheets_path"] = self.sheets
        
        super().__init__(gameObj, self.table, groups[0])
        
        # Create the hp bar of the entity
        self.hpbar_size = (50, 5)
        self.hp_size = 50
        self.hpbar_pos = pg.Vector2(((self.position.x - (self.hpbar_size[0] * 0.5)) + (self.size[0] / 2), self.position.y - 16))
        
        self.hp_bar_table = {"name": "hpBar", "type": "hpBar", "position": {"x": self.hpbar_pos.x, "y": self.hpbar_pos.y}, "size": {"width": self.hpbar_size[0], "height": self.hpbar_size[1]}, 
                             "sheets_path": pg.Surface(self.hpbar_size), "id": self.sprite_id, "priority": self.priority, "obj_name": "hpBar " + str(len(groups[1]))}
        
        self.hp_bar = Sprite(gameObj, self.hp_bar_table, groups[1])
        self.hp_bar.image.fill((0, 255, 0))
        self.hb_color = (0, 182, 0)
        self.gap_color = (82, 128, 96)
        self.show_hpbar = True
        self.is_loosing_hp = False
        self.gap = 0
        self.percent_loose = 0
        self.p_l_2 = 0.30
        self.tick = 0
                
                
    def update(self):
        super().update()
        
        self.hp_bar.state = self.state
        
        if self.action == "moving":
            self.position.y += self.vel_y
            self.position.x += self.vel_x
        
        self.hp_bar.position = pg.Vector2(((self.position.x - (self.hpbar_size[0] * 0.5)) + (self.size[0] / 2), self.position.y - 16))
        
        self.hp_bar.image.fill((0, 0, 0))
        
        if self.show_hpbar:
            if self.is_loosing_hp:
                self.gap = self.hp_size + (((self.hp_loose * self.percent_loose) * self.hpbar_size[0]) / self.base_health)
                
                pg.draw.rect(self.hp_bar.image, self.gap_color, (0, 0, self.gap, self.hpbar_size[1]))
                pg.draw.rect(self.hp_bar.image, self.hb_color, (0, 0, self.hp_size, self.hpbar_size[1]))
                
                if self.p_l_2 > 0.03125:
                    if self.tick == 70:
                        self.tick = 0
                        self.p_l_2 /= 1.5
                        self.percent_loose -= self.p_l_2
                    else:
                        self.tick += 1
                else:
                    self.is_loosing_hp = False
                    self.p_l_2 = 0.30
            else:
                pg.draw.rect(self.hp_bar.image, self.hb_color, (0, 0, self.hp_size, self.hpbar_size[1]))
            
        
    def loose_hp(self, hp_loose):
        
        if self.health > 0:
        
            self.old_hp = self.health
            self.health -= hp_loose
            self.hp_loose = hp_loose
            self.is_loosing_hp = True
            
            self.old_size = self.hp_size
            self.hp_size = (self.health * self.hpbar_size[0]) / self.base_health
            
            self.percent_loose = 0.65
            
    def change_direction(self, new_direction):
        self.old_direction = self.direction
        self.direction = new_direction
        
        
