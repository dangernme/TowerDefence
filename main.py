import pygame as pg
from enemy import Enemy
from world import World
import constants as c

def main():
    pg.init()

    clock = pg.time.Clock()
    screen = pg.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
    pg.display.set_caption("Tower Defence")

    world = World()

    enemy = Enemy(world.waypoints)
    enemy_group = pg.sprite.Group()
    enemy_group.add(enemy)
    run = True

    while run:
        clock.tick(c.FPS)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

        # Update
        enemy_group.update()

        # Draw
        screen.fill((50,50,80))
        world.draw(screen)
        pg.draw.lines(screen, (255,0,0), False, world.waypoints)
        enemy_group.draw(screen)
        pg.display.flip()

    pg.quit()

if __name__ == "__main__":
    main()
