import math
import pygame as pg
import constants as c
from turret_data import TURRET_DATA

class Turret(pg.sprite.Sprite):
    def __init__(self, sprite_sheets, mouse_tile_x, mouse_tile_y):
        super().__init__()
        self.upgrade_level = 1
        self.sprite_sheets = sprite_sheets
        self.mouse_tile_x = mouse_tile_x
        self.mouse_tile_y = mouse_tile_y
        self.selected = False
        self.target = None

        # Position
        self.x = (mouse_tile_x + 0.5) * c.TILE_SIZE
        self.y = (mouse_tile_y + 0.5) * c.TILE_SIZE

        # Animation
        self.animation_list = self.load_images(self.sprite_sheets[self.upgrade_level - 1])
        self.frame_index = 0
        self.cooldown = TURRET_DATA[self.upgrade_level - 1].get('cooldown')
        self.last_shot = pg.time.get_ticks()
        self.angle = 90
        self.original_image = self.animation_list[self.frame_index]
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.update_time = pg.time.get_ticks()

        # Range circle
        self.range = TURRET_DATA[self.upgrade_level - 1].get('range')
        self.range_image = pg.Surface((self.range * 2, self.range * 2))
        self.range_image.set_colorkey((0, 0, 0))
        pg.draw.circle(self.range_image, 'blue', (self.range, self.range), self.range)
        self.range_image.set_alpha(30)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center

    def update(self, enemy_group, world):
        if self.target:
            self.play_animation()
        else:
            if pg.time.get_ticks() - self.last_shot > (self.cooldown / world.game_speed):
                self.pick_target(enemy_group)

    def pick_target(self, enemy_group):
        x_dist = 0
        y_dist = 0
        for enemy in enemy_group:
            if enemy.health > 0:
                x_dist = enemy.pos[0] - self.x
                y_dist = enemy.pos[1] - self.y
                dist = math.sqrt(x_dist ** 2 + y_dist ** 2)
                if dist < self.range:
                    self.target = enemy
                    self.angle = math.degrees(math.atan2(-y_dist, x_dist))
                    self.target.health -= c.DAMAGE
                    break

    def play_animation(self):
        self.original_image = self.animation_list[self.frame_index]

        if pg.time.get_ticks() - self.update_time > c.ANIMATION_DELAY:
            self.update_time = pg.time.get_ticks()
            self.frame_index += 1

            if self.frame_index >= len(self.animation_list):
                self.frame_index = 0
                self.last_shot = pg.time.get_ticks()
                self.target = None

    def load_images(self, sprite_sheet):
        animation_list = []
        size = sprite_sheet.get_height()

        for x in range(c.ANIMATION_STEPS):
            temp_img = sprite_sheet.subsurface(x * size, 0, size, size)
            temp_img = pg.transform.scale_by(temp_img, 0.8)
            animation_list.append(temp_img)

        return animation_list

    def upgrade(self):
        self.upgrade_level += 1
        self.animation_list = self.load_images(self.sprite_sheets[self.upgrade_level - 1])
        self.original_image = self.animation_list[self.frame_index]
        self.range = TURRET_DATA[self.upgrade_level - 1].get('range')
        self.cooldown = TURRET_DATA[self.upgrade_level - 1].get('cooldown')

        # Upgrade range circle
        self.range = TURRET_DATA[self.upgrade_level - 1].get('range')
        self.range_image = pg.Surface((self.range * 2, self.range * 2))
        self.range_image.set_colorkey((0, 0, 0))
        pg.draw.circle(self.range_image, 'blue', (self.range, self.range), self.range)
        self.range_image.set_alpha(30)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center

    def draw(self, surface):
        self.image = pg.transform.rotate(self.original_image, self.angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        if self.selected:
            surface.blit(self.range_image, self.range_rect)
        surface.blit(self.image, self.rect)
