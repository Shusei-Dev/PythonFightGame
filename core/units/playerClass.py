import pygame as pg

from core.units.entityClass import *

class Player(Entity):
    def __init__(self, gameObj, sprite_table, groups):
        super().__init__(gameObj, sprite_table, groups)
        
        self.gameObj = gameObj
        self.table = sprite_table[0]
        
        self.set_animation("forward_idle", [0.4, 0.4])
        
        
    def update(self):
        super().update()
        
        # Player inputs (for moving)
        if self.gameObj.settings.data["control"]["forward"] in self.gameObj.inputs.keys_event:
            if not self.gameObj.inputs.direction_keys["forward"]:
                self.change_direction(self.directions[2])
                self.action = "moving"
                self.gameObj.inputs.direction_keys["forward"] = True
                self.gameObj.inputs.all_directions.append(self.direction)
        else:
            if self.gameObj.inputs.direction_keys["forward"]:
                self.gameObj.inputs.direction_keys["forward"] = False
                self.gameObj.inputs.all_directions.remove("backward")
            
        if self.gameObj.settings.data["control"]["backward"] in self.gameObj.inputs.keys_event:
            if not self.gameObj.inputs.direction_keys["backward"]:
                self.change_direction(self.directions[1])
                self.action = "moving"
                self.gameObj.inputs.direction_keys["backward"] = True
                self.gameObj.inputs.all_directions.append(self.direction)
        else:
            if self.gameObj.inputs.direction_keys["backward"]:
                self.gameObj.inputs.direction_keys["backward"] = False
                self.gameObj.inputs.all_directions.remove("forward")
        
        if self.gameObj.settings.data["control"]["left"] in self.gameObj.inputs.keys_event:
            if not self.gameObj.inputs.direction_keys["left"]:
                self.change_direction(self.directions[3])
                self.action = "moving"
                self.vel_x = self.speed * -1
                self.gameObj.inputs.direction_keys["left"] = True
                self.gameObj.inputs.all_directions.append(self.direction)
        else:
            if self.gameObj.inputs.direction_keys["left"]:
                self.gameObj.inputs.direction_keys["left"] = False
                self.gameObj.inputs.all_directions.remove("left")
            
        if self.gameObj.settings.data["control"]["right"] in self.gameObj.inputs.keys_event:
            if not self.gameObj.inputs.direction_keys["right"]:
                self.change_direction(self.directions[4])
                self.action = "moving"
                self.vel_x = self.speed
                self.gameObj.inputs.direction_keys["right"] = True
                self.gameObj.inputs.all_directions.append(self.direction)
        else:
            if self.gameObj.inputs.direction_keys["right"]:
                self.gameObj.inputs.direction_keys["right"] = False 
                self.gameObj.inputs.all_directions.remove("right")    
                
                
        if self.gameObj.settings.data["control"]["forward"] not in self.gameObj.inputs.keys_event and self.gameObj.settings.data["control"]["backward"] not in self.gameObj.inputs.keys_event and self.gameObj.settings.data["control"]["left"] not in self.gameObj.inputs.keys_event and self.gameObj.settings.data["control"]["right"] not in self.gameObj.inputs.keys_event:
            self.change_direction(self.directions[0])
            self.action = "none"        
         
        
        if self.action == "moving":
            if self.gameObj.inputs.all_directions[-1] == "forward":
                self.vel_y = self.speed 
                
            if self.gameObj.inputs.all_directions[-1] == "backward":
                self.vel_y = self.speed * -1
                
            if self.gameObj.inputs.all_directions[-1] == "left":
                self.vel_x = self.speed * -1
            
            if self.gameObj.inputs.all_directions[-1] == "right":
                self.vel_x = self.speed
            
        
        if self.gameObj.settings.data["control"]["forward"] not in self.gameObj.inputs.keys_event and self.gameObj.settings.data["control"]["backward"] not in self.gameObj.inputs.keys_event:
            self.vel_y = 0
        
        if self.gameObj.settings.data["control"]["left"] not in self.gameObj.inputs.keys_event and self.gameObj.settings.data["control"]["right"] not in self.gameObj.inputs.keys_event:
            self.vel_x = 0
            
        
        # Player animation (for moving and idle)
        if self.action == "moving":
            self.set_animation(self.gameObj.inputs.all_directions[-1], [0.4, 0.4])
             
        if self.direction == self.directions[0]:
            if self.old_direction == self.directions[1]:
                self.set_animation("forward_idle", [0.4, 0.4])
            elif self.old_direction == self.directions[2]:
                self.set_animation("backward_idle", [0.4, 0.4])
            elif self.old_direction == self.directions[3]:
                self.set_animation("left_idle", [0.4, 0.4])
            elif self.old_direction == self.directions[4]:
                self.set_animation("right_idle", [0.4, 0.4])
            