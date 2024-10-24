import json
import pygame as pg

class World:
    def __init__(self):
        self.image = pg.image.load(r'assets\levels\level_01.png').convert_alpha()
        with open('assets/levels/level_01.tmj', 'r', encoding='utf-8') as file:
            self.level_data = json.load(file)
        self.waypoints = []
        self.tile_map = []
        self.process_data()
        self.start = (0, 0)
        self.process_waypoints()

    def process_data(self):
        for layers in self.level_data['layers']:
            if layers['name'] == 'waypoints':
                for obj in layers['objects']:
                    self.waypoint_data = obj['polyline']
                    self.start_x = obj['x']
                    self.start_y = obj['y']
            elif layers['name'] == 'ground':
                self.tile_map = layers['data']

    def process_waypoints(self):
        for point in self.waypoint_data:
            temp_x = point.get('x')
            temp_y = point.get('y')
            self.waypoints.append((temp_x + self.start_x, temp_y + self.start_y))

    def draw(self, surface):
        surface.blit(self.image, (0,0))
