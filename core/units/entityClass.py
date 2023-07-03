import pygame as pg

from core.units.spriteClass import *
from core.misc.spr_sheet_loader import *

class Entity(Sprite):
    
    def __init__(self, gameObj, sprite_table, groups):
        self.gameObj = gameObj
        self.table = sprite_table[0]
        
        # Init the basics of a sprite unit
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
        
        super().__init__(gameObj, name, "entity", position, size, self.sheets, self.sprite_id, self.priority, groups[0], self.gameObj.window.all_sprite)
        
        # Create the hp bar of the entity
        self.hpbar_size = (50, 5)
        self.hp_size = 50
        self.hpbar_pos = pg.Vector2(((self.position.x - (self.hpbar_size[0] * 0.5)) + (self.size[0] / 2), self.position.y - 16))
        self.hp_bar = Sprite(gameObj, "hpBar", "hpBar", self.hpbar_pos, self.hpbar_size, pg.Surface(self.hpbar_size), self.sprite_id, self.priority, groups[1], self.gameObj.window.all_sprite)
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
        
        
