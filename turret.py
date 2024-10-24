import pygame as pg
import constants as c

class Turret(pg.sprite.Sprite):
    def __init__(self, image, mouse_tile_x, mouse_tile_y):
        super().__init__()
        self.mouse_tile_x = mouse_tile_x
        self.mouse_tile_y = mouse_tile_y
        self.x = (mouse_tile_x + 0.5) * c.TILE_SIZE
        self.y = (mouse_tile_y + 0.5) * c.TILE_SIZE
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
