import json

import pygame

def read_json(path):
    f = open(path + '.json', 'r')
    data = json.load(f)
    f.close()
    return data

def load_img(path, colorkey=(0, 0, 0)):
    img = pygame.image.load(path).convert()
    img.set_colorkey(colorkey)
    return img
