import math
import pygame as pg
import constants as c

class Turret(pg.sprite.Sprite):
    def __init__(self, mouse_tile_x, mouse_tile_y, turret_data):
        super().__init__()
        # Position
        self.mouse_tile_x = mouse_tile_x
        self.mouse_tile_y = mouse_tile_y
        self.x = (mouse_tile_x + 0.5) * c.TILE_SIZE
        self.y = (mouse_tile_y + 0.5) * c.TILE_SIZE

        # General
        self.upgrade_level = 1
        self.selected = False
        self.target = None

        # Turret data
        self.turret_data = turret_data
        self.upgrade_max_level = self.turret_data.get('constants').get('levels')
        self.damage = self.turret_data.get('turret_data')[self.upgrade_level - 1].get('damage')
        self.sell_reward = self.turret_data.get('constants').get('sell_reward')
        self.upgrade_costs = self.turret_data.get('constants').get('upgrade_cost')

        # Sound
        self.gun_sound = None
        self.gun_sound_played = False

        # Image
        self.original_image = None
        self.base_image = None
        self.original_base_image = None
        self.image = None
        self.rect = None
        self.base_image_rect = None
        self.sprite_sheets = []

        # Animation
        self.animation_list = []
        self.frame_index = 0
        self.cooldown = self.turret_data.get('turret_data')[self.upgrade_level - 1].get('cooldown')
        self.last_shot = pg.time.get_ticks()
        self.angle = 90
        self.update_time = pg.time.get_ticks()

        # Range circle
        self.range = self.turret_data.get('turret_data')[self.upgrade_level - 1].get('range')
        self.range_image = pg.Surface((self.range * 2, self.range * 2))
        self.range_image.set_colorkey((0, 0, 0))
        pg.draw.circle(self.range_image, 'blue', (self.range, self.range), self.range)
        self.range_image.set_alpha(30)
        self.range_rect = self.range_image.get_rect()

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
                    self.target.health -= self.damage
                    break

    def play_animation(self):
        self.original_image = self.animation_list[self.frame_index]

        if pg.time.get_ticks() - self.update_time > c.ANIMATION_DELAY:
            self.update_time = pg.time.get_ticks()
            self.frame_index += 1

            if self.frame_index == (len(self.animation_list) // 2): # Play the sound halfway through the animation
                if not self.gun_sound_played:
                    self.gun_sound.play()
                    self.gun_sound_played = True

            if self.frame_index >= len(self.animation_list):
                self.frame_index = 0
                self.last_shot = pg.time.get_ticks()
                self.target = None
                self.gun_sound_played = False

    def load_images(self, sprite_sheet):
        animation_list = []
        size = sprite_sheet.get_height()

        for x in range(self.turret_data.get('constants').get('animation_steps')):
            temp_img = sprite_sheet.subsurface(x * size, 0, size, size)
            temp_img = pg.transform.scale_by(temp_img, 0.8)
            animation_list.append(temp_img)

        return animation_list

    def upgrade(self):
        self.upgrade_level += 1
        self.animation_list = self.load_images(self.sprite_sheets[self.upgrade_level - 1])
        self.original_image = self.animation_list[self.frame_index]
        self.range = self.turret_data.get('turret_data')[self.upgrade_level - 1].get('range')
        self.cooldown = self.turret_data.get('turret_data')[self.upgrade_level - 1].get('cooldown')
        self.damage = self.turret_data.get('turret_data')[self.upgrade_level - 1].get('damage')

        # Upgrade range circle
        self.range = self.turret_data.get('turret_data')[self.upgrade_level - 1].get('range')
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

        surface.blit(self.base_image, self.base_image_rect)
        if self.selected:
            surface.blit(self.range_image, self.range_rect)
        surface.blit(self.image, self.rect)
