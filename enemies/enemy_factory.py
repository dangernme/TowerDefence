import pygame as pg
from enemies.enemy import Enemy
from enemies.enemy_data import ENEMY_DATA

class EnemyFactory:
    def __init__(self):
        self.weak_enemy_image = pg.image.load(r'assets\tiles\PNG\Default size\towerDefense_tile245.png').convert_alpha()
        self.medium_enemy_image = pg.image.load(r'assets\tiles\PNG\Default size\towerDefense_tile246.png').convert_alpha()
        self.strong_enemy_image = pg.image.load(r'assets\tiles\PNG\Default size\towerDefense_tile247.png').convert_alpha()
        self.elite_enemy_image = pg.image.load(r'assets\tiles\PNG\Default size\towerDefense_tile248.png').convert_alpha()
        self.plane_weak_enemy_image = pg.image.load(r'assets\tiles\PNG\Default size\towerDefense_tile270.png').convert_alpha()
        self.plane_strong_enemy_image = pg.image.load(r'assets\tiles\PNG\Default size\towerDefense_tile271.png').convert_alpha()

    def create_enemy(self, enemy_type, waypoints):
        new_enemy = Enemy(waypoints, ENEMY_DATA.get(enemy_type), enemy_type)

        if enemy_type == 'weak':
            new_enemy.original_image = self.weak_enemy_image
            new_enemy.original_image = pg.transform.scale_by(new_enemy.original_image, 1.2)
        elif enemy_type == 'medium':
            new_enemy.original_image = self.medium_enemy_image
            new_enemy.original_image = pg.transform.scale_by(new_enemy.original_image, 1.2)
        elif enemy_type == 'strong':
            new_enemy.original_image = self.strong_enemy_image
            new_enemy.original_image = pg.transform.scale_by(new_enemy.original_image, 1.2)
        elif enemy_type == 'elite':
            new_enemy.original_image = self.elite_enemy_image
            new_enemy.original_image = pg.transform.scale_by(new_enemy.original_image, 1.2)
        elif enemy_type == 'plane_weak':
            new_enemy.original_image = self.plane_weak_enemy_image
            new_enemy.original_image = pg.transform.scale_by(new_enemy.original_image, 2)
        elif enemy_type == 'plane_strong':
            new_enemy.original_image = self.plane_strong_enemy_image
            new_enemy.original_image = pg.transform.scale_by(new_enemy.original_image, 2)
        else:
            raise ValueError(f"Unknown enemy type: {enemy_type}")


        new_enemy.image = pg.transform.rotate(new_enemy.original_image, new_enemy.angle)
        new_enemy.rect = new_enemy.image.get_rect()
        new_enemy.rect.center = new_enemy.pos

        return new_enemy
