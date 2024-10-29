import pygame as pg
from enemy import Enemy
from world import World
from turret import Turret
from button import Button
import constants as c

class Game():
    def __init__(self):
        pg.init()
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode((c.SCREEN_WIDTH + c.SIDE_PANEL, c.SCREEN_HEIGHT))
        pg.display.set_caption("Tower Defence")
        self.placing_turret = False
        self.turret_cursor = pg.image.load(r'assets\shakers\Red\Weapons\weapon01.png').convert_alpha()
        self.enemy_group = pg.sprite.Group()
        self.turret_group = pg.sprite.Group()
        self.turret_button = Button(c.SCREEN_WIDTH + 30, 20, 'BUY', 'white', 'blue', True)
        self.cancel_button = Button(c.SCREEN_WIDTH + 30, 100, 'CANCEL', 'white', 'red', False)

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
                    if event.pos[0] < c.SCREEN_WIDTH and event.pos[1] < c.SCREEN_HEIGHT and self.placing_turret:
                        self.create_turret(event.pos)

            # Update
            self.enemy_group.update()
            self.turret_group.update()

            # Draw
            self.screen.fill((50,50,80))

            self.world.draw(self.screen)
            self.enemy_group.draw(self.screen)
            self.turret_group.draw(self.screen)

            if self.turret_button.draw(self.screen):
                self.placing_turret = True
            if self.placing_turret:
                cursor_pos = pg.mouse.get_pos()
                cursor_rect = self.turret_cursor.get_rect()
                cursor_rect.center = cursor_pos
                if cursor_pos[0] < c.SCREEN_WIDTH:
                    self.screen.blit(self.turret_cursor, cursor_rect)
                if self.cancel_button.draw(self.screen):
                    self.placing_turret = False

            pg.display.flip()

        pg.quit()

    def create_turret(self, pos):
        mouse_tile_x = pos[0] // c.TILE_SIZE
        mouse_tile_y = pos[1] // c.TILE_SIZE
        mouse_tile_num = (mouse_tile_y * c.COLS) + mouse_tile_x
        if self.world.tile_map[mouse_tile_num] == 25:
            space_is_free = True
            for turret in self.turret_group:
                if (mouse_tile_x, mouse_tile_y) == (turret.mouse_tile_x, turret.mouse_tile_y):
                    space_is_free = False
            if space_is_free:
                self.turret_group.add(Turret(self.turret_cursor, mouse_tile_x, mouse_tile_y))
