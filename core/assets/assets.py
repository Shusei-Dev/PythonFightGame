import pygame as pg
import json

class Assets:

    def __init__(self, gameObj):
        self.gameObj = gameObj
        
    def load_table(self, table_name):
        with open("core/assets/" + table_name + ".json") as table_file:
            file_contents = table_file.read()
            parsed = json.loads(file_contents)
            return parsed
        
    def get_table_element(self, table, element):
        return table[element]
    
    def get_id(self, table, element):
        return table[element]["id"]
