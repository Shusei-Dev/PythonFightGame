import pygame as pg
import os

from core.misc.io import *
from collections import OrderedDict



class Sprite(pg.sprite.Sprite):

    def __init__(self, gameObj, name, type, position, size, table, sprite_id, layer, group, all_sprite):
        super().__init__(group)

        # Initialize every important element for the sprite obj
        self.gameObj = gameObj
        self.name = name
        self.type = type
        self.org_pos = position
        self.position = position
        self.size = size
        self.table = table
        self._layer = layer
        self.offset = pg.Vector2(0, 0)
        self.state = True
        self.updatable = False

        # Check if its an array of images
        if not isinstance(table, dict):
            # Check if its already a surface
            if isinstance(self.table, pg.Surface):
                self.org_img = self.table
                self.image = self.org_img.copy()
            else:
                self.org_img = load_img(self.table)
                self.image = self.org_img.copy()
        else:
            self.images = {}
            
            # Import all images
            for images in table:
                
                if isinstance(table[images], list):
                    pass
                else:
                    self.images[images] = load_img(table[images])
                    
            self.image = pg.Surface(self.size)
            
        if self.size == None:
            self.size = (self.image.get_width(), self.image.get_height())

        self.rect = self.image.get_rect()
        self.rect.topleft = self.position
        
        self.group = group

        self.sprite_id = str(sprite_id) + "#" + str(len(self.group.sprites()))
        
        self.brightness = 0
        
        all_sprite.add(self)
        

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

    def update(self):
        self.rect.topleft = self.position
        
        if not self.state and self in self.gameObj.window.all_sprite.sprites():
            self.gameObj.window.all_sprite.remove(self)
        
        if self.state and self not in self.gameObj.window.all_sprite.sprites():
            self.gameObj.window.all_sprite.add(self)