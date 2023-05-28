import pygame as pg

from core.units.entityClass import *

class Player(Entity):
    def __init__(self, gameObj, sprite_table, groups):
        super().__init__(gameObj, sprite_table, groups)