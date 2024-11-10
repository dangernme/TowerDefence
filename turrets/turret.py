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
        self.target_selection = 'first'

        # Turret data
        self.turret_data = turret_data
        self.turret_type = self.turret_data.get('constants').get('name')
        self.upgrade_max_level = self.turret_data.get('constants').get('levels')
        self.damage = self.turret_data.get('turret_data')[self.upgrade_level - 1].get('damage')
        self.sell_reward = self.turret_data.get('constants').get('sell_reward')
        self.upgrade_costs = self.turret_data.get('constants').get('upgrade_cost') * self.upgrade_level

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
                if self.target_selection == 'nearest':
                    self.pick_nearest_target(enemy_group)
                elif self.target_selection == 'strongest':
                    self.pick_strongest_target(enemy_group)
                elif self.target_selection == 'first':
                    self.pick_first_target(enemy_group)

    def pick_nearest_target(self, enemy_group):
        nearest_enemy = None
        target_dist_x = 0
        target_dist_y = 0
        for enemy in enemy_group:
            if self.turret_type == 'basic' and enemy.type == 'plane':
                continue
            if enemy.health > 0:
                x_dist = enemy.pos[0] - self.x
                y_dist = enemy.pos[1] - self.y
                dist = math.sqrt(x_dist ** 2 + y_dist ** 2)
                if dist < self.range:
                    if not nearest_enemy:
                        nearest_enemy = enemy
                        target_dist_x = x_dist
                        target_dist_y = y_dist
                    elif dist < math.sqrt((nearest_enemy.pos[0] - self.x) ** 2 + (nearest_enemy.pos[1] - self.y) ** 2):
                        nearest_enemy = enemy
                        target_dist_x = x_dist
                        target_dist_y = y_dist

        if nearest_enemy:
            self.target = nearest_enemy
            self.angle = math.degrees(math.atan2(-target_dist_y, target_dist_x))
            self.target.health -= self.damage

    def pick_first_target(self, enemy_group):
        first_enemy = None
        target_dist_x = 0
        target_dist_y = 0
        for enemy in enemy_group:
            if self.turret_type == 'basic' and enemy.enemy_type in ['plane_weak', 'plane_strong']:
                continue
            if enemy.health > 0:
                x_dist = enemy.pos[0] - self.x
                y_dist = enemy.pos[1] - self.y
                dist = math.sqrt(x_dist ** 2 + y_dist ** 2)
                if dist < self.range:
                    enemy_progress = (pg.time.get_ticks() - enemy.start_time) * enemy.speed
                    if not first_enemy:
                        first_enemy = enemy
                        target_dist_x = x_dist
                        target_dist_y = y_dist
                        target_progress = (pg.time.get_ticks() - first_enemy.start_time) * first_enemy.speed
                    elif enemy_progress > target_progress:
                        first_enemy = enemy
                        target_dist_x = x_dist
                        target_dist_y = y_dist
                        target_progress = (pg.time.get_ticks() - first_enemy.start_time) * first_enemy.speed

        if first_enemy:
            self.target = first_enemy
            self.angle = math.degrees(math.atan2(-target_dist_y, target_dist_x))
            self.target.health -= self.damage

    def pick_strongest_target(self, enemy_group):
        strongest_enemy = None
        target_dist_x = 0
        target_dist_y = 0
        for enemy in enemy_group:
            if self.turret_type == 'basic' and enemy.type == 'plane':
                continue
            if enemy.health > 0:
                x_dist = enemy.pos[0] - self.x
                y_dist = enemy.pos[1] - self.y
                dist = math.sqrt(x_dist ** 2 + y_dist ** 2)
                if dist < self.range:
                    if not strongest_enemy:
                        strongest_enemy = enemy
                        target_dist_x = x_dist
                        target_dist_y = y_dist
                    elif enemy.health > strongest_enemy.health:
                        strongest_enemy = enemy
                        target_dist_x = x_dist
                        target_dist_y = y_dist

        if strongest_enemy:
            self.target = strongest_enemy
            self.angle = math.degrees(math.atan2(-target_dist_y, target_dist_x))
            self.target.health -= self.damage


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
        self.upgrade_costs = math.ceil(self.upgrade_costs * self.upgrade_level * 0.6)
        self.animation_list = self.load_images(self.sprite_sheets[self.upgrade_level - 1])
        self.original_image = self.animation_list[self.frame_index]
        self.range = self.turret_data.get('turret_data')[self.upgrade_level - 1].get('range')
        self.cooldown = self.turret_data.get('turret_data')[self.upgrade_level - 1].get('cooldown')
        self.damage = self.turret_data.get('turret_data')[self.upgrade_level - 1].get('damage')
        self.sell_reward = math.ceil(self.sell_reward * self.upgrade_level * 0.6)

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
