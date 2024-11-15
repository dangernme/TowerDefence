import pygame as pg

class WorldButton():
    def __init__(self):
        self.image = None
        self.rect = None
        self.clicked = False

    def reinit(self, x, y, image):
        self.image = image
        self.image = pg.transform.scale(self.image, (200, 200))

        mask = pg.Surface((200, 200), pg.SRCALPHA)
        pg.draw.rect(mask, (0, 0, 0, 0), mask.get_rect())
        pg.draw.rect(mask, (255, 255, 255, 255), mask.get_rect(), border_radius=10)
        self.image.blit(mask, (0, 0), special_flags=pg.BLEND_RGBA_MIN)

        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, surface):
        action = False
        pos = pg.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] and self.clicked is False:
                self.clicked = True
            if not pg.mouse.get_pressed()[0] and self.clicked:
                action = True
                self.clicked = False

        surface.blit(self.image, self.rect)

        return action
