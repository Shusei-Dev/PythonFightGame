import pygame as pg
from pygame.locals import *
from src.units.playerClass import *


class EntityManager:
    
    def __init__(self, gameObj):
        self.gameObj = gameObj
        
        self.assets = self.gameObj.assets
        
        self.entity_groups = {"player": [], "hpBar": []}
        self.entityTable = self.assets.load_table("entityTable")
        
        self.entity_test = Player(self.gameObj, self.assets.get_table_element(self.entityTable, "player"), [self.entity_groups["player"], self.entity_groups["hpBar"]])
        self.key_c = False
        
       
        
        
    def update(self):
        
        # if "space" in self.gameObj.inputs.keys_event and not self.key_c:
        #     self.entity_test.loose_hp(20)
        #     self.key_c = True
        
        # if "space" not in self.gameObj.inputs.keys_event and self.key_c:
        #     self.key_c = False
        
        
        for groups in self.entity_groups:
            group = self.entity_groups[groups]
            for sprite in group:
                sprite.update()