import pygame as pg
from pygame.locals import *
from core.units.playerClass import *


class entityManager:
    
    def __init__(self, gameObj):
        self.gameObj = gameObj
        self.assets = self.gameObj.assets
        
        self.entity_groups = {"player": pg.sprite.Group(), "hpBar": pg.sprite.Group()}
        self.entityTable = self.assets.load_table("entityTable")
        
        self.entity_test = Player(self.gameObj, self.assets.get_table_element(self.entityTable, "player"), [self.entity_groups["player"], self.entity_groups["hpBar"]])
        self.key_c = False
        
       
        
        
    def update(self):
        
        if "space" in self.gameObj.inputs.keys_event and not self.key_c:
            self.entity_test.loose_hp(20)
            self.key_c = True
        
        if "space" not in self.gameObj.inputs.keys_event and self.key_c:
            self.key_c = False
        
        
        for sprite in self.entity_groups:
            sprite = self.entity_groups[sprite]
            sprite.update()