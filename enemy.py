import math
import pygame as pg
from pygame.math import Vector2

class Enemy(pg.sprite.Sprite):
    def __init__(self, waypoints):
        super().__init__()
        self.angle = 0
        self.speed = 3
        self.waypoints = waypoints
        self.pos = Vector2(self.waypoints[0])
        self.image = pg.image.load(r'assets\Tiles\PNG\Default size\towerDefense_tile245.png').convert_alpha()
        self.image = pg.transform.scale_by(self.image, 1.5)
        self.original_image = self.image
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.target_waypoint = 1
        self.target = None
        self.movement = None

    def update(self):
        self.move()
        self.rotate()

    def move(self):
        if self.target_waypoint < len(self.waypoints):
            self.target = Vector2(self.waypoints[self.target_waypoint])
            self.movement = self.target - self.pos
        else:
            self.kill()

        dist = self.movement.length()
        if dist >= self.speed:
            self.pos += self.movement.normalize() * self.speed
        else:
            if dist != 0:
                self.pos += self.movement.normalize() * dist
            self.target_waypoint += 1

    def rotate(self):
        dist = self.target - self.pos
        self.angle = math.degrees(math.atan2(-dist[1], dist[0]))

        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
