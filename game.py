import json
import pygame as pg
from enemies.enemy_factory import EnemyFactory
from world import World
from button import Button
from world_button import WorldButton
from turrets.turret_factory import TurretFactory
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
        self.run = True
        self.placing_turret = False
        self.selected_turret = None
        self.world = None
        self.level_started = False
        self.game_over = False
        self.game_outcome = 0
        self.confirm_sell = False
        self.turret_type = None
        self.turret_cursor = None
        self.turret_factory = TurretFactory()
        self.enemy_factory = EnemyFactory()

        # Load assets
        self.turret_std_cursor = pg.image.load(r'assets\shakers\Red\Weapons\weapon01.png').convert_alpha()
        self.turret_std_cursor = pg.transform.scale_by(self.turret_std_cursor, 0.8)
        self.turret_laser_cursor = pg.image.load(r'assets\shakers\Blue\Weapons\weapon05.png').convert_alpha()
        self.turret_laser_cursor = pg.transform.scale_by(self.turret_laser_cursor, 0.8)
        self.turret_plasma_cursor = pg.image.load(r'assets\shakers\Purple\Weapons\weapon05.png').convert_alpha()
        self.turret_plasma_cursor = pg.transform.scale_by(self.turret_plasma_cursor, 0.8)
        self.text_font = pg.font.SysFont('Consolas', 24, bold=True)
        self.large_font = pg.font.SysFont('Consolas', 36)

        # Enemies
        self.last_enemy_spawn = pg.time.get_ticks()

        # Sprite setup
        self.enemy_group = pg.sprite.Group()
        self.turret_group = pg.sprite.Group()
        self.buy_basic_gun_button = Button(c.SCREEN_WIDTH + 70, 100, f'BASIC GUN ${self.turret_factory.get_turret_costs('basic')}', 'white', 'red', True)
        self.buy_laser_gun_button = Button(c.SCREEN_WIDTH + 70, 150, f'LASER GUN ${self.turret_factory.get_turret_costs('laser')}', 'white', 'blue', True)
        self.buy_plasma_gun_button = Button(c.SCREEN_WIDTH + 70, 200, f'PLASMA GUN ${self.turret_factory.get_turret_costs('plasma')}', 'white', 'purple', True)
        self.cancel_button = Button(c.SCREEN_WIDTH + 70, 250, 'CANCEL', 'white', 'red', True)
        self.upgrade_button = Button(c.SCREEN_WIDTH + 70, 300, 'UPGRADE', 'orange', 'black', True)
        self.first_target_button = Button(c.SCREEN_WIDTH + 70, 350, 'FIRST TARGET', 'black', 'blue', True)
        self.nearest_target_button = Button(c.SCREEN_WIDTH + 70, 400, 'NEAR TARGET', 'black', 'green', True)
        self.strongest_target_button = Button(c.SCREEN_WIDTH + 70, 450, 'STRONG TARGET', 'black', 'green', True)
        self.sell_turret_button = Button(c.SCREEN_WIDTH + 70, 700, 'SELL TURRET', 'red', 'black', True)
        self.confirm_sell_turret_button = Button(c.SCREEN_WIDTH + 70, 750, 'CONFIRM', 'red', 'black', True)
        self.fast_forward_button = Button(c.SCREEN_WIDTH + 70, 850, 'FAST', 'red', 'blue', False)
        self.start_button = Button(c.SCREEN_WIDTH + 70, 900, 'START', 'green', 'black', True)
        self.okay_button = Button(410, 400, 'OK', 'black', 'red', True)

        # World selection setup
        self.world_selection = True
        self.world_number = 0
        self.world_buttons = []
        for _ in range(c.TOTAL_WORLDS):
            self.world_buttons.append(WorldButton())

        # World setup
        self.world_images = []
        self.world_data_files = []

        for world_num in range(1, c.TOTAL_WORLDS + 1):
            world_image_path = f'assets/worlds/world_{world_num:02}.png'
            world_data_path = f'assets/worlds/world_{world_num:02}.tmj'
            self.world_images.append(pg.image.load(world_image_path).convert_alpha())
            with open(world_data_path, 'r', encoding='utf-8') as file:
                self.world_data_files.append(json.load(file))

    def draw_text(self, text, font, text_color, pos):
        image = font.render(text, True, text_color)
        self.screen.blit(image, pos)

    def run_game(self):
        self.run = True

        while self.run:
            self.clock.tick(c.FPS)

            if self.world_selection:
                self.screen.fill('black')
                self.draw_text('SELECT WORLD', self.large_font, 'white', (500, 20))
                for i in range(c.TOTAL_WORLDS):
                    self.world_buttons[i].reinit(50 + (i * 250), 100, self.world_images[i])
                    if self.world_buttons[i].draw(self.screen):
                        print('action')
                        self.world_number = i
                        self.world = World(self.world_images[self.world_number], self.world_data_files[self.world_number])
                        self.world.process_data()
                        self.world.process_enemies()
                        self.world_selection = False
                        break
            else:

                if not self.game_over:
                    if self.world.health <= 0:
                        self.world.health = 0
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
                            print(c.FAST_FORWARD_SPEED)

                        decreasing_spawn_cooldown = max(c.MAX_SPAWN_COOLDOWN / self.world.level, c.MIN_SPAWN_COOLDOWN)
                        if pg.time.get_ticks() - self.last_enemy_spawn > decreasing_spawn_cooldown / self.world.game_speed:
                            if self.world.spawned_enemies < len(self.world.enemy_list):
                                enemy_type = self.world.enemy_list[self.world.spawned_enemies]
                                enemy = self.enemy_factory.create_enemy(enemy_type, self.world.waypoints)
                                self.enemy_group.add(enemy)
                                self.world.spawned_enemies += 1
                                self.last_enemy_spawn = pg.time.get_ticks()

                    if self.world.check_level_complete():
                        self.load_next_level()

                    # Draw buttons
                    if self.buy_basic_gun_button.draw(self.screen):
                        self.placing_turret = True
                        self.turret_type = 'basic'

                    if self.buy_laser_gun_button.draw(self.screen):
                        self.placing_turret = True
                        self.turret_type = 'laser'

                    if self.buy_plasma_gun_button.draw(self.screen):
                        self.placing_turret = True
                        self.turret_type = 'plasma'

                    if self.placing_turret:
                        if self.turret_type == 'basic':
                            self.turret_cursor = self.turret_std_cursor
                        elif self.turret_type == 'laser':
                            self.turret_cursor = self.turret_laser_cursor
                        elif self.turret_type == 'plasma':
                            self.turret_cursor = self.turret_plasma_cursor
                        cursor_pos = pg.mouse.get_pos()
                        cursor_rect = self.turret_cursor.get_rect()
                        cursor_rect.center = cursor_pos
                        if cursor_pos[0] < c.SCREEN_WIDTH:
                            self.screen.blit(self.turret_cursor, cursor_rect)

                        if self.cancel_button.draw(self.screen):
                            self.placing_turret = False

                    if self.selected_turret:
                        if self.selected_turret.upgrade_level < self.selected_turret.upgrade_max_level:
                            self.upgrade_button.text = f'UPGRADE ${self.selected_turret.upgrade_costs}'

                            if self.upgrade_button.draw(self.screen):
                                if self.world.money >= self.selected_turret.upgrade_costs:
                                    self.world.money -= self.selected_turret.upgrade_costs
                                    self.selected_turret.upgrade()

                        if self.first_target_button.draw(self.screen):
                            self.selected_turret.target_selection = 'first'

                        elif self.nearest_target_button.draw(self.screen):
                            self.selected_turret.target_selection = 'nearest'

                        elif self.strongest_target_button.draw(self.screen):
                            self.selected_turret.target_selection = 'strongest'

                        if self.selected_turret.target_selection == 'nearest':
                            self.first_target_button.background_color = 'green'
                            self.nearest_target_button.background_color = 'blue'
                            self.strongest_target_button.background_color = 'green'
                        elif self.selected_turret.target_selection == 'first':
                            self.first_target_button.background_color = 'blue'
                            self.nearest_target_button.background_color = 'green'
                            self.strongest_target_button.background_color = 'green'
                        elif self.selected_turret.target_selection == 'strongest':
                            self.first_target_button.background_color = 'green'
                            self.nearest_target_button.background_color = 'green'
                            self.strongest_target_button.background_color = 'blue'

                        self.sell_turret_button.text = f'SELL TURRET ${self.selected_turret.sell_reward}'
                        if self.sell_turret_button.draw(self.screen):
                            self.confirm_sell = True

                        if self.confirm_sell:
                            if self.confirm_sell_turret_button.draw(self.screen):
                                self.world.money += self.selected_turret.sell_reward
                                self.selected_turret.kill()
                                self.confirm_sell = False
                                self.clear_selection()

                else:
                    self.handle_game_over()

            self.event_handler()

            pg.display.flip()

        pg.quit()

    def load_next_level(self):
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

    def handle_game_over(self):
        pg.draw.rect(self.screen, 'dodgerblue', (300, 300, 400, 200), border_radius=30)
        if self.game_outcome == -1:
            self.draw_text('GAME OVER', self.large_font, 'grey0', (410, 320))
        elif self.game_outcome == 1:
            self.draw_text('YOU WIN', self.large_font, 'grey0', (430, 320))

        if self.okay_button.draw(self.screen):
            self.reset()

    def reset(self):
        self.world = None
        self.game_over = False
        self.level_started = False
        self.placing_turret = False
        self.selected_turret = None
        self.last_enemy_spawn = pg.time.get_ticks()
        self.enemy_group.empty()
        self.turret_group.empty()
        self.world_selection = True

    def create_turret(self, mouse_pos):
        mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
        mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
        mouse_tile_num = (mouse_tile_y * c.COLS) + mouse_tile_x
        if self.world.tile_map[mouse_tile_num] in c.BUILDABLE_TILES:
            space_is_free = True
            for turret in self.turret_group:
                if (mouse_tile_x, mouse_tile_y) == (turret.mouse_tile_x, turret.mouse_tile_y):
                    space_is_free = False
            if space_is_free:
                self.turret_group.add(self.turret_factory.create_turret(self.turret_type, mouse_tile_x, mouse_tile_y))
                self.world.money -= self.turret_factory.get_turret_costs(self.turret_type)

    def select_turret(self, mouse_pos):
        mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
        mouse_tile_y = mouse_pos[1] // c.TILE_SIZE

        for turret in self.turret_group:
            if (mouse_tile_x, mouse_tile_y) == (turret.mouse_tile_x, turret.mouse_tile_y):
                return turret

        return None

    def event_handler(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.run = False
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 3:
                if self.selected_turret:
                    self.clear_selection()
                if self.placing_turret:
                    self.placing_turret = False
                    self.turret_cursor = None
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pg.mouse.get_pos()
                if mouse_pos[0] < c.SCREEN_WIDTH and mouse_pos[1] < c.SCREEN_HEIGHT:
                    self.clear_selection()
                    if self.placing_turret:
                        if self.world.money >= self.turret_factory.get_turret_costs(self.turret_type):
                            self.create_turret(mouse_pos)
                    else:
                        self.selected_turret = self.select_turret(mouse_pos)


    def clear_selection(self):
        for turret in self.turret_group:
            turret.selected = False
        self.selected_turret = None
        self.confirm_sell = False
