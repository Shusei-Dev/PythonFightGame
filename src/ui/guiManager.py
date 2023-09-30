import pygame as pg

from src.ui.btnClass import *
from src.ui.windowClass import *

class GuiManager:

    def __init__(self, gameObj):

        self.gameObj = gameObj
        self.assets = self.gameObj.assets

        self.gui_groups = {"btn_group": [], "window_group": [], "popup_group": [], "text_input_group": []}
        self.uiTable = self.assets.load_table("uiTable")
        

        #self.btn_test = Button(self.gameObj, "btn_test", pg.Vector2(0, 0), None, self.gameObj.assets.btn_test, 0, 1, self.gui_groups["btn_group"])
        #self.org_color = [[74, 74, 74], [106, 106, 106], [128, 128, 128]]
            
        self.windowTest = WindowClass(self.gameObj, self.assets.get_table_element(self.uiTable, "window_test"), self.gui_groups)
        self.windowTest2 = WindowClass(self.gameObj, self.assets.get_table_element(self.uiTable, "window_test2"), self.gui_groups)


    def update(self):
        
        for groups in self.gui_groups:
            group = self.gui_groups[groups]
            for sprite in group:
                sprite.update()
                
            
            # Test the brightness of a sprite
            #for sprites in sprite.sprites():
                
                # if sprites.name == "btn_test":
                #     if sprites.events["mouse_on"]:
                #         if sprites.brightness <= 44:
                #             sprites.brightness += 2
                #             sprites.change_bright(self.org_color, sprites.brightness)
                #             self.org_color = [[74 + sprites.brightness, 74 + sprites.brightness, 74 + sprites.brightness], [106 + sprites.brightness, 106 + sprites.brightness, 106 + sprites.brightness], [128 + sprites.brightness, 128 + sprites.brightness, 128 + sprites.brightness]]
                #     else:
                #         sprites.reset_img()
                #         sprites.brightness = 0
                #         self.org_color = [[74, 74, 74], [106, 106, 106], [128, 128, 128]]
                
