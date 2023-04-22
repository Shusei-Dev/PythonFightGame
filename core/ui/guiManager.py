import pygame as pg

from core.ui.btnClass import *
from core.ui.windowClass import *

class guiManager:

    def __init__(self, gameObj):

        self.gameObj = gameObj

        self.gui_groups = {"btn_group": pg.sprite.Group(), "window_group": pg.sprite.Group(), "popup_group": pg.sprite.Group()}
        self.uiTable = self.gameObj.assets.load_table("uiTable")

        self.btn_test = Button(self.gameObj, "btn_test", pg.Vector2(0, 0), None, self.gameObj.assets.btn_test, 0, 1, self.gui_groups["btn_group"])
        self.org_color = [[74, 74, 74], [106, 106, 106], [128, 128, 128]]
            
        self.windowTest = WindowClass(self.gameObj, "window_test", pg.Vector2(100, 100), (352, 160), self.gameObj.assets.get_table_element(self.uiTable, "basic_window"), [self.gui_groups["window_group"]], "window_test")
        self.windowTest2 = WindowClass(self.gameObj, "window_test2", pg.Vector2(500, 500), (144, 64), self.gameObj.assets.get_table_element(self.uiTable, "basic_window2"), [self.gui_groups["window_group"], self.gui_groups["popup_group"]], "this is a test window it retract if its too large")
        self.windowTest3 = WindowClass(self.gameObj, "window_test3", pg.Vector2(350, 350), (240, 240), self.gameObj.assets.get_table_element(self.uiTable, "basic_window"), [self.gui_groups["window_group"]], "window_test3")

    def update(self):
        
        for sprite in self.gui_groups:
            sprite = self.gui_groups[sprite]
            sprite.update()
            
            # Test the brightness of a sprite
            for sprites in sprite.sprites():
                
                if sprites.name == "btn_test":
                    if sprites.events["mouse_on"]:
                        if sprites.brightness <= 44:
                            sprites.brightness += 2
                            sprites.change_bright(self.org_color, sprites.brightness)
                            self.org_color = [[74 + sprites.brightness, 74 + sprites.brightness, 74 + sprites.brightness], [106 + sprites.brightness, 106 + sprites.brightness, 106 + sprites.brightness], [128 + sprites.brightness, 128 + sprites.brightness, 128 + sprites.brightness]]
                    else:
                        sprites.reset_img()
                        sprites.brightness = 0
                        self.org_color = [[74, 74, 74], [106, 106, 106], [128, 128, 128]]
                        
