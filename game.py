import pygame as pg
from enemy import Enemy
from world import World
from turret import Turret
import constants as c

class Game():
    def __init__(self):
        pg.init()
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
        pg.display.set_caption("Tower Defence")

        self.turret_image = pg.image.load(r'assets\Tiles\PNG\Default size\towerDefense_tile250.png').convert_alpha()
        self.enemy_group = pg.sprite.Group()
        self.turret_group = pg.sprite.Group()

        self.world = World()

    def run(self):
        enemy = Enemy(self.world.waypoints)
        self.enemy_group.add(enemy)

        run = True

        while run:
            self.clock.tick(c.FPS)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    if event.pos[0] < c.SCREEN_WIDTH and event.pos[1] < c.SCREEN_HEIGHT:
                        self.create_turret(event.pos)


            # Update
            self.enemy_group.update()
            self.turret_group.update()

            # Draw
            self.screen.fill((50,50,80))

            self.world.draw(self.screen)
            self.enemy_group.draw(self.screen)
            self.turret_group.draw(self.screen)
            pg.display.flip()

        pg.quit()

    def create_turret(self, pos):
        mouse_tile_x = pos[0] // c.TILE_SIZE
        mouse_tile_y = pos[1] // c.TILE_SIZE
        mouse_tile_num = (mouse_tile_y * c.COLS) + mouse_tile_x
        if self.world.tile_map[mouse_tile_num] == 25:
            self.turret_group.add(Turret(self.turret_image, mouse_tile_x, mouse_tile_y))
