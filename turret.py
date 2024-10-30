import pygame as pg
import constants as c

class Turret(pg.sprite.Sprite):
    def __init__(self, sprite_sheet, mouse_tile_x, mouse_tile_y):
        super().__init__()

        self.sprite_sheet = sprite_sheet
        self.mouse_tile_x = mouse_tile_x
        self.mouse_tile_y = mouse_tile_y
        self.selected = False

        # Position
        self.x = (mouse_tile_x + 0.5) * c.TILE_SIZE
        self.y = (mouse_tile_y + 0.5) * c.TILE_SIZE

        # Animation
        self.animation_list = self.load_images()
        self.frame_index = 0
        self.cooldown = 1500
        self.last_shot = pg.time.get_ticks()
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.update_time = pg.time.get_ticks()

        # Range circle
        self.range = 90
        self.range_image = pg.Surface((self.range * 2, self.range * 2))
        self.range_image.set_colorkey((0, 0, 0))
        pg.draw.circle(self.range_image, 'blue', (self.range, self.range), self.range)
        self.range_image.set_alpha(30)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center

    def update(self):
        if pg.time.get_ticks() - self.last_shot > self.cooldown:
            self.play_animation()

    def play_animation(self):
        self.image = self.animation_list[self.frame_index]
        if pg.time.get_ticks() - self.update_time > c.ANIMATION_DELAY:
            self.update_time = pg.time.get_ticks()
            self.frame_index += 1

            if self.frame_index >= len(self.animation_list):
                self.frame_index = 0
                self.last_shot = pg.time.get_ticks()

    def load_images(self):
        animation_list = []
        size = self.sprite_sheet.get_height()

        for x in range(c.ANIMATION_STEPS):
            temp_img = self.sprite_sheet.subsurface(x * size, 0, size, size)
            temp_img = pg.transform.scale_by(temp_img, 0.8)
            animation_list.append(temp_img)

        return animation_list

    def draw(self, surface):
        if self.selected:
            surface.blit(self.range_image, self.range_rect)
        surface.blit(self.image, self.rect)
