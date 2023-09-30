import pygame as pg

class Chunk:
    
    def __init__(self, id=int(), position=pg.Vector2(), elements=list()):
        self.id = id
        self.position = position
        self.elements = elements
        
        
def load_chunk(chunk_map, player_pos):
    chunk_map = chunk_map
    player_pos = player_pos
    
    #for chunks in chunk_map.keys():
        
    