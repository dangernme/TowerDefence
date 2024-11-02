import json
import random
import pygame as pg
from enemy_data import ENEMY_SPAWN_DATA
import constants as c

class World:
    def __init__(self):
        self.image = pg.image.load(r'assets\levels\level_01.png').convert_alpha()
        with open('assets/levels/level_01.tmj', 'r', encoding='utf-8') as file:
            self.level_data = json.load(file)
        self.waypoints = []
        self.level = 1
        self.health = c.HEALTH
        self.money = c.MONEY
        self.tile_map = []
        self.start = (0, 0)
        self.enemy_list = []
        self.waypoint_data = []
        self.start_x = 0
        self.start_y = 0
        self.spawned_enemies = 0
        self.killed_enemies = 0
        self.missed_enemies = 0
        self.game_speed = 1

    def process_data(self):
        for layers in self.level_data['layers']:
            if layers['name'] == 'waypoints':
                for obj in layers['objects']:
                    self.waypoint_data = obj['polyline']
                    self.start_x = obj['x']
                    self.start_y = obj['y']
            elif layers['name'] == 'ground':
                self.tile_map = layers['data']

        self.process_waypoints()

    def process_waypoints(self):
        for point in self.waypoint_data:
            temp_x = point.get('x')
            temp_y = point.get('y')
            self.waypoints.append((temp_x + self.start_x, temp_y + self.start_y))

    def process_enemies(self):
        enemies = ENEMY_SPAWN_DATA[self.level - 1]
        for enemy_type in enemies:
            enemies_to_spawn = enemies[enemy_type]
            for _ in range(enemies_to_spawn):
                self.enemy_list.append(enemy_type)

        random.shuffle(self.enemy_list)

    def check_level_complete(self):
        if self.killed_enemies + self.missed_enemies == len(self.enemy_list):
            return True
        return False

    def reset_level(self):
        self.enemy_list = []
        self.spawned_enemies = 0
        self.killed_enemies = 0
        self.missed_enemies = 0

    def draw(self, surface):
        surface.blit(self.image, (0,0))
