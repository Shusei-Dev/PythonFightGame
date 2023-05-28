import pygame as pg

from core.units.entityClass import *


class entityManager:
    
    def __init__(self, gameObj):
        self.gameObj = gameObj
        self.assets = self.gameObj.assets
        
        self.entity_groups = {"player": pg.sprite.Group()}
        self.entityTable = self.assets.load_table("entityTable")
        
        self.entity_test = Entity(self.gameObj, self.assets.get_table_element(self.entityTable, "player"), [self.entity_groups["player"]])
        
        
        
    def update(self):
        
        for sprite in self.entity_groups:
            sprite = self.entity_groups[sprite]
            sprite.update()