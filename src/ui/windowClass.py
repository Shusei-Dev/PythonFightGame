import pygame as pg
import numpy as np
import re

from src.units.spriteClass import *
from src.misc.font_loader import * 
from src.misc.spr_sheet_loader import *

#elements
from src.ui.btnClass import *
from src.ui.popupClass import *
from src.ui.textInputClass import *

class WindowClass(Sprite):
    
    def __init__(self, gameObj, sprite_table, groups):
        
        self.gameObj = gameObj
        
        self.sprite_table = sprite_table[0]
        self.sprite_table["obj_name"] = sprite_table[1]
        size = (self.sprite_table["size"]["width"], self.sprite_table["size"]["height"])
        self.bg_color = eval(self.sprite_table["bg_color"])
        self.bar_color = eval(self.sprite_table["bar_color"])
        
        #TODO: Change the method to spritesheet
        self.animation = load_sheet(self.sprite_table["sheets_path"], 16, 16, 9)
        self.sprite_table["sheets_path"] = self.animation
        
        self.groups = groups
        
        self.pos_when_click = pg.Vector2(0, 0)
        self.is_draggble = True
        self.draggble = False
        self.on_front = False
        self.bg_window = False
        
        self.focused = False
        
        self.elements_list = []
        
        self.debug = 0
        
        # Check the size of the window
        if size[0] < 48 and size[1] < 48:
            print("ERROR the size of the window is too small !")
            self.gameObj.quit()
        
        elif (size[0] / 16) % 1 == 0.0 and (size[1] / 16) % 1 == 0.0:
            super().__init__(gameObj, self.sprite_table, self.groups["window_group"])
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
        self.image.blit(self.animation["img9"], (self.size[0] - 13, 3))
        
        # Create the collison of the cross
        self.cross_collide = pg.Rect(self.position.x + self.size[0] - 12, self.position.y + 3, 10, 10)
        
        # Draw the text on the bar
        self.window_name = self.name
        self.new_name = str(self.name)
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
            
            self.bubble_sprite = Popup(self.gameObj, self.name + "_bubble", "popup", pg.Vector2(0, 0), self.window_name_bubble.get_size(), self.window_name_bubble, 2, self.layer_nmb + 1, self.groups["popup_group"])
            
            self.bubble_sprite.state = False
        
        # Draw the window name text
        self.image.blit(self.window_b_text, (4, 4))
        
        # Create the window text rect only if we change it
        if self.change_name:
            self.window_text_rect = pg.Rect(self.position[0] + 4, self.position[1] + 4, self.window_b_text.get_size()[0], self.window_b_text.get_size()[1])
        
        # Drawing the corner
        self.image.blit(self.animation["img1"], (0, 0))
        self.image.blit(self.animation["img2"], (self.size[0] - 16, 0))
        self.image.blit(self.animation["img3"], (0, self.size[1] - 16))
        self.image.blit(self.animation["img4"], (self.size[0] - 16, self.size[1] - 16))
        
        # Drawing the edges
        c_x, c_y = 16, -6
        for i in range(2):
            for x in range(self.window_size[0] - 2):
                if i == 0:
                    self.image.blit(self.animation["img5"], (c_x, c_y))
                else:
                    self.image.blit(self.animation["img6"], (c_x, c_y))
                c_x += 16
                
            c_x = 16
            c_y = (16 * (self.window_size[1] - 1)) + 7
            
        c_x, c_y = -6, 16
        
        for i in range(2):
            for y in range(self.window_size[1] - 2):
                if i == 0:
                    self.image.blit(self.animation["img7"], (c_x, c_y))
                else:
                    self.image.blit(self.animation["img8"], (c_x, c_y))
                c_y += 16
                
            c_y = 16
            c_x = (16 * (self.window_size[0] - 1)) +6
           
        # get all elements tables  
        try:
            self.elements = self.sprite_table["elements"]
            self.elements_tables = []
            self.assets_table = self.gameObj.assets.load_table("uiTable")
            
            
            for element in self.elements:
                self.elements_tables.append(self.gameObj.assets.get_table_element(self.assets_table, element))
            
            
            # Init all element if needeed
            last_element_offset = pg.Vector2()
            windows_corner_offset = pg.Vector2(self.position.x + 5, self.position.y + 18)
            content_element_position = []
            for element in self.elements_tables:
                content_element = element[0]
                org_pos_x = 0
                org_pos_y = 0
                org_pos_x += content_element["position"]["x"]
                org_pos_y += content_element["position"]["y"]
                
                if content_element["type"] == "element":
                    
                    if content_element["element_type"] == "text_input":
                        
                        if content_element["size"]["width"] <= windows_corner_offset.x + self.size[0]:
                            
                            element_pos = content_element["position"]
                           
                            if last_element_offset.x == 0 and last_element_offset.y == 0:
                                element_pos["x"] += windows_corner_offset.x
                                element_pos["y"] += windows_corner_offset.y
                                
                            if last_element_offset.x != 0 and element_pos["x"] != 0 and element_pos["y"] == 0:
                                element_pos["y"] += windows_corner_offset.y
                            
                            if last_element_offset.x != 0 and org_pos_x == 0 and org_pos_y != 0:
                                
                                element_pos["x"] += windows_corner_offset.x
                            
                            if last_element_offset.x != 0 and org_pos_y == 0:
                                if content_element["position"]["x"] + last_element_offset.x < self.size[0]:
                                    element_pos["x"] += last_element_offset.x
                                    
                            if last_element_offset.x != 0 and org_pos_x == 0 and org_pos_y != 0:
                                element_pos["y"] += last_element_offset.y
                                    
                            if last_element_offset.x != 0 and org_pos_y != 0 and org_pos_x != 0:
                                if content_element["position"]["x"] + last_element_offset.x < self.size[0] and content_element["position"]["y"] + last_element_offset.y < self.size[1]:
                                    element_pos["x"] += last_element_offset.x
                                    element_pos["y"] += last_element_offset.y
                            
                            
                            last_element_offset.x = element_pos["x"] + content_element["size"]["width"]
                            last_element_offset.y = element_pos["y"] + content_element["size"]["height"]
                            
                            content_element["priority"] += self.org_layer
                            content_element["position"] = element_pos
                            
                            element_obj = TextInput(self.gameObj, element, self.groups["text_input_group"])
                            
                            
                            element_obj.offset.x = element_pos["x"] - self.position.x
                            element_obj.offset.y = element_pos["y"] - self.position.y
                            
                            self.elements_list.append(element_obj)
                     
                    content_element_position.append(content_element["position"])
                        
        except Exception as err:
            pass
        
            
    def update(self):
        
        # Closing the window when the cross is pressed
        if self.cross_collide.collidepoint(self.gameObj.inputs.mouse_event.POS):
            if self.gameObj.inputs.mouse_event.LEFT_CLICK[0] and self.gameObj.inputs.mouse_event.LEFT_CLICK[1] <= 5 and self.state and self.focused:
                self.state = False
                for element in self.elements_list:
                    element.state = False
                    
        # Check if the window is behing another one (with size and pos)
        windows_collision = pg.sprite.spritecollide(self, self.groups["window_group"], False)
        for cursor in windows_collision:
            for windows in windows_collision:
                if windows != cursor:
                    #print(cursor.layer_nmb, windows.layer_nmb)
                    if cursor.position.x > windows.position.x and cursor.position.x + cursor.size[0] < windows.position.x + windows.size[0] and cursor.position.y > windows.position.y and cursor.position.y + cursor.size[1] < windows.position.y + windows.size[1] and cursor.layer_nmb < windows.layer_nmb and windows.state != False:
                        cursor.bg_window = True
                    else:
                        pass
                        cursor.bg_window = False
        
        # Show the full name of the window when the mouse is on it
        if self.change_name:
            if self.window_text_rect.collidepoint(self.gameObj.inputs.mouse_event.POS) and not self.gameObj.inputs.mouse_event.LEFT_CLICK[0] and self.state:
                if self.focused:
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
                    if self.elements_list != []:
                        if self.change_name:
                            new_list = []
                            for element in self.elements_list:
                                new_list.append(element)
                            new_list.append(self.bubble_sprite)
                            new_list.append(self)
                            
                            self.gameObj.layer_manager.moves_to_front(new_list)
                        else:
                            new_list = [self]
                            for element in self.elements_list:
                                new_list.append(element)
                            
                            self.gameObj.layer_manager.moves_to_front(new_list)
                    else:
                        if self.change_name:
                            self.gameObj.layer_manager.moves_to_front([self.bubble_sprite, self])
                        else:
                            self.gameObj.layer_manager.move_to_front(self)
                        
                    self.gameObj.layer_manager.print_all_layers()
                    
                    for windows in self.groups["window_group"]:
                        if windows != self:
                            windows.focused = False
                            windows.layer_nmb = self.gameObj.layer_manager.get_layer_of_sprite(windows)
      
                    self.pos_when_click.x = self.gameObj.inputs.mouse_event.POS[0]
                    self.pos_when_click.y = self.gameObj.inputs.mouse_event.POS[1]
                
                self.draggble = True

            if not self.gameObj.inputs.mouse_event.LEFT_CLICK[0] and self.draggble:
                
                self.draggble = False
                self.org_pos.x = self.position.x
                self.org_pos.y = self.position.y
                
                for element in self.elements_list:
                    element.org_pos.x = element.position.x
                    element.org_pos.y = element.position.y
                
        if self.draggble:
            self.focused = True
                   
        # Move the window to the cursor             
        if self.draggble and self.focused:
            
            self.offset.x = self.org_pos.x + (self.gameObj.inputs.mouse_event.POS[0] - self.pos_when_click.x)
            self.offset.y = self.org_pos.y + (self.gameObj.inputs.mouse_event.POS[1] - self.pos_when_click.y)
            self.position = self.offset
            self.rect_bar.topleft = self.position
            self.cross_collide.topleft = ((self.position.x + self.size[0]) - 13, self.position.y + 3)
            if self.change_name:
                self.window_text_rect.topleft = (self.position.x + 4, self.position.y + 4)  
            
            # Change pos of elements
            for element in self.elements_list:
                element.position.x = self.position.x + element.offset.x
                element.position.y = self.position.y + element.offset.y
              
        super().update()
            
            
    def change_size_text(self, text):
        self.text = FontText(self.sprite_table["font"], 5, (255, 255, 255), text, True)
        if self.text.get_size()[0] + 42 > self.size[0] + 4:
            if text[-2] == " ":
                return text[:-2]
            else:
                return text[:-1]
        