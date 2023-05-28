import pygame as pg
import time
import win32ui

class Window():

    def __init__(self, gameObj, size, name, version, fps):
        pg.init()

        self.gameObj = gameObj
        self.base_resolution = size
        self.scale_factor = 10
        self.screen_size = (pg.display.Info().current_w, pg.display.Info().current_h)
        self.name = name
        self.version = version

        self.window = pg.display.set_mode(self.base_resolution)
        self.display = pg.Surface(self.base_resolution)

        pg.display.set_caption(self.name + " v" + str(self.version))

        self.fps = 60
        self.dt = 0.01
        self.last_frame_end = time.time()
        self.master_clock = 0
        
        self.all_sprite = pg.sprite.LayeredUpdates()

        self.running = True

    def update(self):
        # TODO: Work on the focusing system
        #self.focus_windows = win32ui.GetForegroundWindow().GetWindowText()
        
        # Scale if needed
       
        
        self.window.blit(self.display, (0, 0))
        print(self.display.get_width())

        pg.display.update()

        t = time.time()
        self.dt = t - self.last_frame_end
        self.last_frame_end = t
        self.master_clock += self.dt
        

        self.display.fill((0, 0, 0))

        
