import pygame as pg

class World:
    def __init__(self):
        self.image = pg.image.load(r'assets\level_01\level_01.png').convert_alpha()

    def draw(self, surface):
        surface.blit(self.image, (0,0))
