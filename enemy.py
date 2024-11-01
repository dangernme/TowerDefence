import math
import pygame as pg
from pygame.math import Vector2
import constants as c
from enemy_data import ENEMY_DATA

class Enemy(pg.sprite.Sprite):
    def __init__(self, enemy_type, waypoints, images):
        super().__init__()
        self.angle = 0
        self.speed = ENEMY_DATA.get(enemy_type)['speed']
        self.health = ENEMY_DATA.get(enemy_type)['health']
        self.waypoints = waypoints
        self.pos = Vector2(self.waypoints[0])
        self.original_image = images.get(enemy_type)
        self.original_image = pg.transform.scale_by(self.original_image, 1.5)
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.target_waypoint = 1
        self.target = None
        self.movement = None

    def update(self, world):
        self.move(world)
        self.rotate()
        self.check_alive(world)

    def move(self, world):
        if self.target_waypoint < len(self.waypoints):
            self.target = Vector2(self.waypoints[self.target_waypoint])
            self.movement = self.target - self.pos
        else:
            self.kill()
            world.health -= 1


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

    def check_alive(self, world):
        if self.health <= 0:
            world.money += c.KILL_REWARD
            self.kill()
