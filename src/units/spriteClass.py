import pygame as pg
import os

from src.misc.io import *
from collections import OrderedDict



class Sprite(pg.sprite.Sprite):

    def __init__(self, gameObj, sprite_table, group):
        super().__init__()

        # Initialize every important element for the sprite obj
        self.gameObj = gameObj
        self.sprite_table = sprite_table
        self.name = self.sprite_table["name"]
        self.obj_name = self.sprite_table["obj_name"]
        self.type = self.sprite_table["type"]
        self.org_pos = pg.Vector2(self.sprite_table["position"]["x"], self.sprite_table["position"]["y"])
        self.position = pg.Vector2(self.sprite_table["position"]["x"], self.sprite_table["position"]["y"])
        
        self.size = (self.sprite_table["size"]["width"], self.sprite_table["size"]["height"])
        self.sheets = self.sprite_table["sheets_path"]
        self.layer_nmb = self.sprite_table["priority"]
        self.org_layer = self.sprite_table["priority"]
        self.sprite_id = self.sprite_table["id"]
        self.offset = pg.Vector2(0, 0)
        self.old_state = True
        self.state = True
        self.state_change = False
        self.updatable = False
        
        # Animation variable
        self.animation_state = ""
        self.animation_choose = "None"
        self.animation_spr = {}
        self.animation_c = -1
        self.animation_reverse = False
        self.last_tick = 0
        self.is_reverse = False
        
        # Camera variable
        self.camera_moveble = True

        # Check if its an array of images
        if not isinstance(self.sheets, dict):
            # Check if its already a surface
            if isinstance(self.sheets, pg.Surface):
                self.org_img = self.sheets
                self.image = self.org_img.copy()
            else:
                self.org_img = load_img(self.sheets)
                self.image = self.org_img.copy()
        else:
            self.images = self.sheets    
            self.image = pg.Surface(self.size)
            
        try:
            self.org_images_list = {}
            self.images_list = {}
            
            for images in self.images:
                img_list = []
                try:
                    # Check if its multiple sheets to create an dict of list
                    for i in self.images[images]:
                        img_list.append(self.images[images][i])
                        self.org_images_list[images] = img_list  
                        self.images_list[images] = img_list  
                except:
                    # Will only create one list
                    img_list.append(self.images[images])
                    self.images_list = img_list
                    self.org_images_list = img_list
        except:
            pass
        
            
        if self.size == None:
            self.size = (self.image.get_width(), self.image.get_height())

        self.rect = self.image.get_rect()
        self.rect.topleft = self.position
        
        self.group = group

        self.group.append(self)

        self.sprite_id = str(self.sprite_id) + "#" + str(len(self.group))
        
        self.brightness = 0
        
        self.gameObj.layer_manager.add_layer(self.org_layer)
        self.gameObj.layer_manager.layers_table[self.org_layer].add_sprite(self, True)
            
        

    def change_bright(self, colors, bright_lvl):
        for bright in colors:
            self.image = self.palette_swap(bright, (bright[0] + bright_lvl, bright[1] + bright_lvl, bright[2] + bright_lvl))
        
        self.image.set_colorkey((0, 0, 0))
        
    def reset_img(self):
        self.image = self.org_img.copy()

    def palette_swap(self, old_color, new_color):
        self.img_copy = pg.Surface(self.image.get_size())
        self.img_copy.fill(new_color)
        self.image.set_colorkey(old_color)
        self.img_copy.blit(self.image, (0, 0))
        return self.img_copy
    
    def set_animation(self, animation_name, time_list, reverse=False):
        self.animation_spr[animation_name] = []
        self.animation_choose = animation_name
        
        self.animation_reverse = reverse
        
        for spr in self.images_list[animation_name]:
            self.animation_spr[animation_name].append(spr)
            
        self.animation_spr[animation_name] += [time_list]
                
                
    def update(self):
        '''
        TODO Working on the scaling
        print(self.org_pos, self.name)
        self.position.x = self.org_pos.x * self.gameObj.window.scale_factor
        self.position.y = self.org_pos.y * self.gameObj.window.scale_factor
        '''
        
        if self.state == self.old_state:
            self.state_change = False
        else: 
            self.old_state = self.state
            self.state_change = True
        
        self.rect.topleft = self.position
        
        # ---- Show the sprite on screen or not ----
        if self.state_change:
        
            self.gameObj.layer_manager.layers_table[self.layer_nmb].change_state(self)
            
        # --------
            
            
        # ---- Animation Update ----
        if self.animation_choose != "None" and len(self.animation_spr) >= 1:
            self.animation_list = self.animation_spr[self.animation_choose]
            
            if not self.animation_c >= len(self.animation_list) - 1 and not self.is_reverse:
                if self.last_tick != 0:
                    self.time_past = round(self.gameObj.window.master_clock - self.last_tick, 1)
                    self.time_next = self.animation_list[-1][self.animation_c]
                    
                    if self.time_past >= self.time_next:
                        if self.animation_c + 1 < len(self.animation_list) - 1:
                            self.animation_c += 1
                            self.last_tick = self.gameObj.window.master_clock
                        else:
                            if not self.animation_reverse:
                                self.animation_c = -1
                           
                else:
                    self.animation_c += 1
                    self.last_tick = self.gameObj.window.master_clock
            
            if self.animation_reverse:
                if self.animation_c == len(self.animation_list) - 2:
                    self.is_reverse = True
                    
                if self.animation_c != 0 and self.is_reverse:
                    self.time_past = round(self.gameObj.window.master_clock - self.last_tick, 1)
                    self.time_next = self.animation_list[-1][self.animation_c]
                
                    if self.time_past >= self.time_next:
                        if self.animation_c - 1 >= 0:
                            self.animation_c -= 1
                            self.last_tick = self.gameObj.window.master_clock
                else:
                    self.is_reverse = False
                    
            self.image.fill((0, 0, 0, 0))
            if self.animation_c == -1:
                self.size = self.animation_list[self.animation_c + 1].get_size()
                self.image.blit(self.animation_list[self.animation_c + 1].convert_alpha(), (0, 0))
            else:
                self.size = self.animation_list[self.animation_c].get_size()
                self.image.blit(self.animation_list[self.animation_c].convert_alpha(), (0, 0))
        # --------