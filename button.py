import pygame as pg

class Button():
    def __init__(self, x, y, text, text_color, background_color, single_click):
        self.rect = pg.Rect(x, y, 200, 40)
        self.text_color = text_color
        self.background_color = background_color
        self.text = text
        self.single_click = single_click
        self.clicked = False

        self.font = pg.font.Font(None, 30)
        self.text_surf = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)
        self.pressed = False

    def draw(self, surface):
        self.text_surf = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)
        action = False
        pos = pg.mouse.get_pos()

        if self.single_click and self.rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] and self.pressed is False:
                self.pressed = True
            elif not pg.mouse.get_pressed()[0] and self.pressed:
                action = True
                self.pressed = False

        elif not self.single_click and self.rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0]:
                action = True

        pg.draw.rect(surface, self.background_color, self.rect, border_radius=10)
        surface.blit(self.text_surf, self.text_rect)

        return action
