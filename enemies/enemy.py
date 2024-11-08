import math
import pygame as pg
from pygame.math import Vector2

class Enemy(pg.sprite.Sprite):
    def __init__(self, waypoints, enemy_data):
        super().__init__()
        self.enemy_data = enemy_data
        self.angle = 0
        self.start_time = pg.time.get_ticks()
        self.speed = self.enemy_data.get('speed')
        self.health = self.enemy_data.get('health')
        self.reward = self.enemy_data.get('reward')
        self.waypoints = waypoints
        self.pos = Vector2(self.waypoints[0])
        self.original_image = None
        self.image = None
        self.rect = None
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
            world.missed_enemies += 1
            world.health -= 1

        dist = self.movement.length()
        if dist >= (self.speed * world.game_speed):
            self.pos += self.movement.normalize() * self.speed  * world.game_speed
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
            world.money += self.reward
            self.kill()
            world.killed_enemies += 1
