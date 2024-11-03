import pygame as pg
from enemy import Enemy
from world import World
from turret import Turret
from button import Button
from turret_data import TURRET_DATA_STD_GUN, TURRET_DATA_LASER_GUN
import constants as c

class Game():
    def __init__(self):
        # General setup
        pg.init()
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode((c.SCREEN_WIDTH + c.SIDE_PANEL, c.SCREEN_HEIGHT))
        pg.display.set_caption("Tower Defence")
        pg.mixer.init()

        # Game variables
        self.placing_turret = False
        self.selected_turret = None
        self.level_started = False
        self.game_over = False
        self.game_outcome = 0
        self.turret_type = None
        self.gun_sound = None
        self.turret_cursor = None

        # Load assets
        self.turret_std_sprite_sheets = []
        for x in range(1, TURRET_DATA_STD_GUN.get('constants').get('levels') + 1):
            self.turret_sheet = pg.image.load(rf'assets\shakers\Red\Weapons\turret_01_mk{x}.png').convert_alpha()
            self.turret_std_sprite_sheets.append(self.turret_sheet)

        self.turret_laser_sprite_sheets = []
        for x in range(1, TURRET_DATA_LASER_GUN.get('constants').get('levels') + 1):
            self.turret_sheet = pg.image.load(rf'assets\shakers\Blue\Weapons\turret_02_mk{x}.png').convert_alpha()
            self.turret_laser_sprite_sheets.append(self.turret_sheet)

        self.turret_std_cursor = pg.image.load(r'assets\shakers\Red\Weapons\weapon01.png').convert_alpha()
        self.turret_std_cursor = pg.transform.scale_by(self.turret_std_cursor, 0.8)
        self.turret_std_sound = pg.mixer.Sound(r'assets\sounds\tock.wav')

        self.turret_laser_cursor = pg.image.load(r'assets\shakers\Blue\Weapons\weapon01.png').convert_alpha()
        self.turret_laser_cursor = pg.transform.scale_by(self.turret_laser_cursor, 0.8)
        self.turret_laser_sound = pg.mixer.Sound(r'assets\sounds\laser_fire.wav')
        self.turret_data = None
        self.turret_sprite_sheets = []

        self.text_font = pg.font.SysFont('Consolas', 24, bold=True)
        self.large_font = pg.font.SysFont('Consolas', 36)

        # Enemies
        self.last_enemy_spawn = pg.time.get_ticks()

        self.enemy_images = {
            'weak': pg.image.load(r'assets\tiles\PNG\Default size\towerDefense_tile245.png').convert_alpha(),
            'medium': pg.image.load(r'assets\tiles\PNG\Default size\towerDefense_tile246.png').convert_alpha(),
            'strong': pg.image.load(r'assets\tiles\PNG\Default size\towerDefense_tile247.png').convert_alpha(),
            'elite': pg.image.load(r'assets\tiles\PNG\Default size\towerDefense_tile248.png').convert_alpha(),
            'plane': pg.image.load(r'assets\tiles\PNG\Default size\towerDefense_tile271.png').convert_alpha()
        }

        # Sprite setup
        self.enemy_group = pg.sprite.Group()
        self.turret_group = pg.sprite.Group()
        self.buy_std_gun_button = Button(c.SCREEN_WIDTH + 30, 80, 'STD GUN', 'white', 'blue', True)
        self.buy_laser_gun_button = Button(c.SCREEN_WIDTH + 30, 160, 'LASER GUN', 'white', 'blue', True)
        self.cancel_button = Button(c.SCREEN_WIDTH + 180, 80, 'CANCEL', 'white', 'red', True)
        self.upgrade_button = Button(c.SCREEN_WIDTH + 30, 320, 'UPGRADE', 'orange', 'blue', True)
        self.start_button = Button(c.SCREEN_WIDTH + 180, 160, 'START', 'green', 'black', True)
        self.fast_forward_button = Button(c.SCREEN_WIDTH + 30, 240, 'FF', 'red', 'blue', False)
        self.sell_turret_button = Button(c.SCREEN_WIDTH + 180, 240, 'SELL', 'red', 'black', True)
        self.restart_button = Button(440, 400, 'RESTART', 'black', 'red', True)

        self.world = World()
        self.world.process_data()
        self.world.process_enemies()

    def draw_text(self, text, font, text_color, pos):
        image = font.render(text, True, text_color)
        self.screen.blit(image, pos)

    def run(self):
        run = True

        while run:
            self.clock.tick(c.FPS)
            total_hit_points = 0
            for enemy in self.enemy_group:
                total_hit_points += enemy.health

            if not self.game_over:
                if self.world.health <= 0:
                    self.game_over = True
                    self.game_outcome = -1

                # Update
                self.enemy_group.update(self.world)
                self.turret_group.update(self.enemy_group, self.world)

                # Highlight selected turret
                if self.selected_turret:
                    self.selected_turret.selected = True

                # Draw
                self.screen.fill((50,50,80))

                self.world.draw(self.screen)
                self.enemy_group.draw(self.screen)

                self.draw_text(f'\u2665 {self.world.health}', self.text_font, 'white', (c.SCREEN_WIDTH + 30, 10))
                self.draw_text(f'$ {self.world.money}', self.text_font, 'white', (c.SCREEN_WIDTH + 30, 30))
                self.draw_text(f'L {self.world.level}/{c.TOTAL_LEVELS}', self.text_font, 'white', (c.SCREEN_WIDTH + 30, 50))
                self.draw_text(f'HP {total_hit_points}', self.text_font, 'white', (c.SCREEN_WIDTH + 120, 10))

                for turret in self.turret_group:
                    turret.draw(self.screen)

                # Spawn enemies
                if not self.level_started:
                    if self.start_button.draw(self.screen):
                        self.level_started = True
                else:
                    # Fast forward option
                    self.world.game_speed = 1
                    if self.fast_forward_button.draw(self.screen):
                        self.world.game_speed = c.FAST_FORWARD_SPEED

                    if pg.time.get_ticks() - self.last_enemy_spawn > c.SPAWN_COOLDOWN:
                        if self.world.spawned_enemies < len(self.world.enemy_list):
                            enemy_type = self.world.enemy_list[self.world.spawned_enemies]
                            enemy = Enemy(enemy_type, self.world.waypoints, self.enemy_images)
                            self.enemy_group.add(enemy)
                            self.world.spawned_enemies += 1
                            self.last_enemy_spawn = pg.time.get_ticks()

                if self.world.check_level_complete():
                    self.world.level += 1
                    if self.world.level <= c.TOTAL_LEVELS:
                        self.world.money += c.LEVEL_COMPLETE_REWARD
                        self.level_started = False
                        self.last_enemy_spawn = pg.time.get_ticks()
                        self.world.reset_level()
                        self.world.process_enemies()
                    else:
                        self.game_over = True
                        self.game_outcome = 1

                # Draw buttons
                if self.buy_std_gun_button.draw(self.screen):
                    self.placing_turret = True
                    self.turret_type = 'std_gun'
                    self.turret_data = TURRET_DATA_STD_GUN
                    self.turret_sprite_sheets = self.turret_std_sprite_sheets
                    self.gun_sound = self.turret_std_sound

                if self.buy_laser_gun_button.draw(self.screen):
                    self.placing_turret = True
                    self.turret_type = 'laser_gun'
                    self.turret_data = TURRET_DATA_LASER_GUN
                    self.turret_sprite_sheets = self.turret_laser_sprite_sheets
                    self.gun_sound = self.turret_laser_sound

                if self.placing_turret:
                    if self.turret_type == 'std_gun':
                        self.turret_cursor = self.turret_std_cursor
                    elif self.turret_type == 'laser_gun':
                        self.turret_cursor = self.turret_laser_cursor
                    cursor_pos = pg.mouse.get_pos()
                    cursor_rect = self.turret_cursor.get_rect()
                    cursor_rect.center = cursor_pos
                    if cursor_pos[0] < c.SCREEN_WIDTH:
                        self.screen.blit(self.turret_cursor, cursor_rect)

                    if self.cancel_button.draw(self.screen):
                        self.placing_turret = False

                if self.selected_turret:
                    if self.selected_turret.upgrade_level < self.selected_turret.upgrade_max_level:
                        if self.upgrade_button.draw(self.screen):
                            if self.world.money >= self.selected_turret.upgrade_costs:
                                self.selected_turret.upgrade()
                                self.world.money -= self.selected_turret.upgrade_costs

                    if self.sell_turret_button.draw(self.screen):
                        self.world.money += self.selected_turret.sell_reward * self.selected_turret.upgrade_level
                        self.selected_turret.kill()
            else:
                pg.draw.rect(self.screen, 'dodgerblue', (300, 300, 400, 200), border_radius=30)
                if self.game_outcome == -1:
                    self.draw_text('GAME OVER', self.large_font, 'grey0', (410, 320))
                elif self.game_outcome == 1:
                    self.draw_text('YOU WIN', self.large_font, 'grey0', (410, 320))

                if self.restart_button.draw(self.screen):
                    self.game_over = False
                    self.level_started = False
                    self.placing_turret = False
                    self.selected_turret = None
                    self.last_enemy_spawn = pg.time.get_ticks()
                    self.world = World()
                    self.world.process_data()
                    self.world.process_enemies()
                    self.enemy_group.empty()
                    self.turret_group.empty()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 3:
                    if self.selected_turret:
                        self.clear_selection()
                        self.selected_turret = None
                    if self.placing_turret:
                        self.placing_turret = False
                        self.turret_cursor = None
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pg.mouse.get_pos()
                    if mouse_pos[0] < c.SCREEN_WIDTH and mouse_pos[1] < c.SCREEN_HEIGHT:
                        self.selected_turret = None
                        self.clear_selection()
                        if self.placing_turret:
                            if self.world.money >= self.turret_data.get('constants').get('buy_cost'):
                                self.create_turret(mouse_pos, self.turret_data)
                        else:
                            self.selected_turret = self.select_turret(mouse_pos)
            pg.display.flip()

        pg.quit()

    def create_turret(self, mouse_pos, turret_data):
        mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
        mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
        mouse_tile_num = (mouse_tile_y * c.COLS) + mouse_tile_x
        if self.world.tile_map[mouse_tile_num] == 25:
            space_is_free = True
            for turret in self.turret_group:
                if (mouse_tile_x, mouse_tile_y) == (turret.mouse_tile_x, turret.mouse_tile_y):
                    space_is_free = False
            if space_is_free:
                self.turret_group.add(Turret(self.turret_sprite_sheets, mouse_tile_x, mouse_tile_y, turret_data, self.gun_sound))
                self.world.money -= self.turret_data.get('constants').get('buy_cost')

    def select_turret(self, mouse_pos):
        mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
        mouse_tile_y = mouse_pos[1] // c.TILE_SIZE

        for turret in self.turret_group:
            if (mouse_tile_x, mouse_tile_y) == (turret.mouse_tile_x, turret.mouse_tile_y):
                return turret

        return None

    def clear_selection(self):
        for turret in self.turret_group:
            turret.selected = False
