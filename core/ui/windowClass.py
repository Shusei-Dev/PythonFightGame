import pygame as pg
import numpy as np
import re

from core.units.spriteClass import *
from core.ui.btnClass import *
from core.misc.font_loader import * 
from core.ui.popupClass import *

class WindowClass(Sprite):
    
    def __init__(self, gameObj, name, position, size, sprite_table, groups, window_name):
        
        self.gameObj = gameObj
        
        self.sprite_table = sprite_table
        
        self.bg_color = eval(self.sprite_table["bg_color"])
        
        self.bar_color = eval(self.sprite_table["bar_color"])
        self.priority = int(self.sprite_table["priority"])
        self.animation = self.sprite_table["images"]
        self.sprite_id = self.sprite_table["id"]
        
        self.groups = groups
        
        self.pos_when_click = pg.Vector2(0, 0)
        self.is_draggble = True
        self.draggble = False
        self.on_front = False
        self.bg_window = False
        
        self.focus_win = False
        
        # Check the size of the window
        if size[0] < 48 and size[1] < 48:
            print("ERROR the size of the window is too small !")
            self.gameObj.quit()
        
        elif (size[0] / 16) % 1 == 0.0 and (size[1] / 16) % 1 == 0.0:
            super().__init__(gameObj, name, "window", position, size, self.animation, self.sprite_id, self.priority, groups[0], self.gameObj.window.all_sprite)
        else:
            print("ERROR the size is not a good format !")
            self.gameObj.quit()
            
        self.window_size = (int(self.size[0] / 16), int(self.size[1] / 16))
        
        # Draw the bg color
        pg.draw.rect(self.image, (self.bg_color), (2, 2, self.size[0] - 4, self.size[1] - 4))
        
        # Draw the bar
        pg.draw.rect(self.image, self.bar_color, (2, 2, self.size[0] - 4, 14))
        if (self.bar_color[0] + self.bar_color[1] + self.bar_color[2]) - 90 < 0:
            print("Cant change the brightness of the bar")
        else:
            pg.draw.line(self.image, (self.bar_color[0] - 30, self.bar_color[1] - 30, self.bar_color[2] - 30), (2, 14), (self.size[0] - 4, 14), 3)
            
        # Create the rect obj of the bar
        self.rect_bar = pg.Rect(self.position.x, self.position.y, self.size[0], 14)
        
        # Draw the cross
        self.image.blit(self.images["cross"], (self.size[0] - 13, 3))
        
        # Create the collison of the cross
        self.cross_collide = pg.Rect(self.position.x + self.size[0] - 12, self.position.y + 3, 10, 10)
        
        # Draw the text on the bar
        self.window_name = window_name
        self.new_name = str(window_name)
        self.window_b_text = FontText(self.sprite_table["font"], 5, (255, 255, 255), self.new_name, True)
        self.change_name = False
        
        
        # Check if the window name is too large, if its so we retract the name
        while self.window_b_text.get_size()[0] + 42 > self.size[0] + 4:
            self.change_name = True
            self.new_name = self.change_size_text(self.new_name)
            self.window_b_text = FontText(self.sprite_table["font"], 5, (255, 255, 255), self.new_name, True)
        
        if self.change_name:
            self.new_name = self.new_name + "..."
            self.window_b_text = FontText(self.sprite_table["font"], 5, (255, 255, 255), self.new_name, True)
        
        # Create the bubble name
        if self.change_name:
            self.window_bublle_text = FontText(self.sprite_table["font"], 5, (255, 255, 255), self.window_name, True)
            self.window_name_bubble = pg.Surface((self.window_bublle_text.get_size()[0] + 8, self.window_bublle_text.get_size()[1] + 8))
            self.window_name_bubble.fill((0, 0, 0))
            self.window_name_bubble.blit(self.window_bublle_text, (4, 4))
            
            self.bubble_sprite = Popup(self.gameObj, self.name + "_bubble", "popup", pg.Vector2(0, 0), self.window_name_bubble.get_size(), self.window_name_bubble, 2, self.priority + 1, groups[1])
            
            self.bubble_sprite.state = False
        
        # Draw the window name text
        self.image.blit(self.window_b_text, (4, 4))
        
        # Create the window text rect only if we change it
        if self.change_name:
            self.window_text_rect = pg.Rect(self.position[0] + 4, self.position[1] + 4, self.window_b_text.get_size()[0], self.window_b_text.get_size()[1])
        
        # Drawing the corner
        self.image.blit(self.images["left_top"], (0, 0))
        self.image.blit(self.images["right_top"], (self.size[0] - 16, 0))
        self.image.blit(self.images["left_bot"], (0, self.size[1] - 16))
        self.image.blit(self.images["right_bot"], (self.size[0] - 16, self.size[1] - 16))
        
        # Drawing the edges
        c_x, c_y = 16, -6
        for i in range(2):
            for x in range(self.window_size[0] - 2):
                if i == 0:
                    self.image.blit(self.images["top"], (c_x, c_y))
                else:
                    self.image.blit(self.images["bot"], (c_x, c_y))
                c_x += 16
                
            c_x = 16
            c_y = (16 * (self.window_size[1] - 1)) + 6
            
        c_x, c_y = -6, 16
        
        for i in range(2):
            for y in range(self.window_size[1] - 2):
                if i == 0:
                    self.image.blit(self.images["left"], (c_x, c_y))
                else:
                    self.image.blit(self.images["right"], (c_x, c_y))
                c_y += 16
                
            c_y = 16
            c_x = (16 * (self.window_size[0] - 1)) +6
            
    def update(self):
        
        # Closing the window when the cross is pressed
        if self.cross_collide.collidepoint(self.gameObj.inputs.mouse_event.POS):
            if self.gameObj.inputs.mouse_event.LEFT_CLICK[0] and self.gameObj.inputs.mouse_event.LEFT_CLICK[1] <= 5 and self.state:
                self.state = False 
        
        # Check if the window is front or not
        if self.gameObj.window.all_sprite.get_layer_of_sprite(self) == self.gameObj.window.all_sprite.get_top_layer():
            self.on_front = True
        else:
            self.on_front = False
            
        # Check if the window is behing another one (with size and pos)
        windows_collision = pg.sprite.spritecollide(self, self.groups[0], False)
        
        

        
        # Show the full name of the window when the mouse is on it
        if self.change_name:
            if self.window_text_rect.collidepoint(self.gameObj.inputs.mouse_event.POS) and not self.gameObj.inputs.mouse_event.LEFT_CLICK[0]:
                if self.on_front:
                    self.bubble_sprite.position.x = self.gameObj.inputs.mouse_event.POS[0] - (self.bubble_sprite.size[0] / 2)
                    self.bubble_sprite.position.y = self.gameObj.inputs.mouse_event.POS[1] - 20
                    self.bubble_sprite.state = True
            else:
                self.bubble_sprite.state = False
                
        # Drag update
        if self.rect_bar.collidepoint(self.gameObj.inputs.mouse_event.POS):
            if self.gameObj.inputs.mouse_event.LEFT_CLICK[0] and self.gameObj.inputs.mouse_event.LEFT_CLICK[1] <= 5 and self.state and self.is_draggble and not self.bg_window:
                if self.draggble == False:
                    # Set the window who has been grabbed to the front layer
                    self.gameObj.window.all_sprite.move_to_front(self)
                    for windows in self.groups[0]:
                        if windows != self:
                            self.gameObj.window.all_sprite.move_to_back(windows)
                                    
                    self.pos_when_click.x = self.gameObj.inputs.mouse_event.POS[0]
                    self.pos_when_click.y = self.gameObj.inputs.mouse_event.POS[1]
                
                self.draggble = True
            
            if not self.gameObj.inputs.mouse_event.LEFT_CLICK[0] and self.draggble:
                self.draggble = False
                self.org_pos.x = self.position.x
                self.org_pos.y = self.position.y
                        
        if self.draggble and self.on_front:
            self.offset.x = self.org_pos.x + (self.gameObj.inputs.mouse_event.POS[0] - self.pos_when_click.x)
            self.offset.y = self.org_pos.y + (self.gameObj.inputs.mouse_event.POS[1] - self.pos_when_click.y)
            self.position = self.offset
            self.rect_bar.topleft = self.position
            self.cross_collide.topleft = ((self.position.x + self.size[0]) - 13, self.position.y + 3)
            if self.change_name:
                self.window_text_rect.topleft = (self.position.x + 4, self.position.y + 4)
                
        super().update()
            
            
    def change_size_text(self, text):
        self.text = FontText(self.sprite_table["font"], 5, (255, 255, 255), text, True)
        if self.text.get_size()[0] + 42 > self.size[0] + 4:
            if text[-2] == " ":
                return text[:-2]
            else:
                return text[:-1]
        