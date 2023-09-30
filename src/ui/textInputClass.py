import pygame as pg
from src.ui.btnClass import *
from src.misc.font_loader import *


class TextInput(Button):
    
    def __init__(self, gameObj, sprite_table, group):
        self.gameObj = gameObj
            
        self.sprite_table = sprite_table[0]
    
        size = (self.sprite_table["size"]["width"], self.sprite_table["size"]["height"])
        self.border_color = eval(self.sprite_table["border_color"])
        self.text_box_color = eval(self.sprite_table["text_box_color"])
        
        self.surface = pg.Surface(size).convert_alpha()
    
        self.surface.fill((0, 0, 0, 0))
        pg.draw.rect(self.surface, self.border_color, (0, 0, size[0], size[1]), 1)
        pg.draw.rect(self.surface, self.text_box_color, (1, 1, size[0] - 2, size[1] - 2))

        self.sprite_table["obj_name"] = sprite_table[1]
        self.sprite_table["sheets_path"] = self.surface
        
        self.input_focus = False
        
        super().__init__(gameObj, self.sprite_table, group)
        
        self.org_input = pg.Surface((self.size[0], self.size[1]))
        self.org_input.blit(self.image, (0, 0))
        self.ticks = 0
        self.text_input = ""
        self.showed_text = ""
        self.printed = False
        self.added_char = False
        self.next_char_tick = 0
        self.last_char_tick = 0
        self.add_bar = False
        

    def update(self):
        
        if self.state:
            
            if self.events["btn_pressed"] == "Left":
                self.input_focus = True
            
            if self.events["btn_pressed"] == "Null" and self.gameObj.inputs.mouse_event.LEFT_CLICK[0]:
                self.input_focus = False
            
            if self.input_focus:
                
                for input in self.gameObj.inputs.keys_event:
                    
                    if self.gameObj.inputs.keys_event[input] <= self.last_char_tick:
                        self.added_char = False
                    
                    if self.gameObj.inputs.keys_event[input] >= 350 and self.added_char:
                        self.added_char = False
                        
                    if self.added_char == False and self.next_char_tick == 40:
                        if input.isalpha() and len(input) == 1:
                            self.text_input += input
                            self.last_char_tick = self.gameObj.inputs.keys_event[input]
                            self.added_char = True
                        elif input == "space":
                            self.text_input += " "
                            self.last_char_tick = self.gameObj.inputs.keys_event[input]
                            self.added_char = True
                        elif input == "backspace":
                            self.text_input = self.text_input[:-1]
                            self.last_char_tick = self.gameObj.inputs.keys_event[input]
                            self.added_char = True
                    
                    if self.next_char_tick < 40:
                        self.next_char_tick += 1
                    else:
                        self.next_char_tick = 0
                
                           
                if self.ticks == 0:
                    self.showed_text += "|"
                    self.add_bar = True
                elif self.ticks == 400:
                    self.showed_text = self.showed_text.replace("|", "")
                    self.add_bar = True
                
                if self.ticks != 800:
                    self.ticks += 1
                else:
                    self.ticks = 0
                    
                if self.add_bar: 
                    self.image.fill((0,0,0))
                    self.image.blit(self.org_input, (0,0))
                    self.image.blit(FontText(self.sprite_table["font"], 11, (255, 255, 255), self.showed_text, True).convert_alpha(), (2, 2))
                print(self.text_input)
            else:
                self.image.fill((0,0,0))
                self.image.blit(self.org_input, (0,0))
                self.image.blit(FontText(self.sprite_table["font"], 11, (255, 255, 255), self.showed_text, True).convert_alpha(), (2, 2))
                    
        

        
        super().update()

