import pygame as pg

from core.units.spriteClass import *

class Button(Sprite):

    def __init__(self, gameObj, name, position, size, animation, sprite_id, priority, group):
        super().__init__(gameObj, name, "button", position, size, animation, sprite_id, priority, group, gameObj.window.all_sprite)

        self.gameObj = gameObj

        self.events = {"btn_pressed": "Null", "mouse_on": False}
        self.clicked = False


    def update(self):
        if self.state:
            self.mouse_rect = pg.Rect(self.gameObj.inputs.mouse_event.POS[0], self.gameObj.inputs.mouse_event.POS[1], 1, 1)
            
            # Check if the mouse is on the btn
            if self.rect.colliderect(self.mouse_rect):
                self.events["mouse_on"] = True
            else:
                self.events["mouse_on"] = False
            
            # Check for the LEFT or RIGHT click on the btn
            if self.events["mouse_on"]:
                if self.gameObj.inputs.mouse_event.LEFT_CLICK[0] and self.events["btn_pressed"] == "Null" and self.clicked == False and self.gameObj.inputs.mouse_event.LEFT_CLICK[1] <= 5:
                    self.events["btn_pressed"] = "Left"
                    self.clicked = True

                if self.gameObj.inputs.mouse_event.RIGHT_CLICK[0] and self.events["btn_pressed"] == "Null" and self.clicked == False and self.gameObj.inputs.mouse_event.RIGHT_CLICK[1] <= 5:
                    self.events["btn_pressed"] = "Right"
                    self.clicked = True
            else:
                self.events["btn_pressed"] = "Null"
                    
            if not self.gameObj.inputs.mouse_event.LEFT_CLICK[0] and not self.gameObj.inputs.mouse_event.RIGHT_CLICK[0]:
                self.events["btn_pressed"] = "Null"
                self.clicked = False
                
                
        super().update()
                
    
                
