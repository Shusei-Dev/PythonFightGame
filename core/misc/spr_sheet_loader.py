from core.misc.io import *
import pygame as pg

def load_sheet(path=str, spr_width=int, spr_height=int, max_sprite=int):
     
    sprite_sheet = load_img(path)
    img_size = sprite_sheet.get_size()
    
    c_x = int(img_size[0] / spr_width)
    c_y = int(img_size[0] / spr_height)
    
    sprites_img = {}
    
    pos_x, pos_y = 0, 0
    c = 1
    for y in range(1, c_y + 1):
        for x in range(1, c_x + 1):
            if c - 1 < max_sprite:   
                new_sprite = pg.Surface((spr_width, spr_height), pygame.SRCALPHA)
                new_sprite.blit(sprite_sheet, (0, 0), (pos_x, pos_y, spr_width, spr_height))
                new_sprite.convert_alpha()
                sprites_img["img" + str(c)] = new_sprite
                c += 1
                pos_x = spr_width * x
            else:
                break
        pos_x = 0
        pos_y = spr_height * y
        
    return sprites_img
    
