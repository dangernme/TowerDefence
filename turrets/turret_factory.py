import pygame as pg
from turrets.turret_data import TURRET_DATA_BASIC_GUN, TURRET_DATA_LASER_GUN
from turrets.turret import Turret

class TurretFactory:
    def __init__(self):
        # Load basic turret assets
        self.turret_basic_sprite_sheets = []
        for x in range(1, TURRET_DATA_BASIC_GUN.get('constants').get('levels') + 1):
            self.turret_sheet = pg.image.load(rf'assets\shakers\Red\Weapons\turret_01_mk{x}.png').convert_alpha()
            self.turret_basic_sprite_sheets.append(self.turret_sheet)
        self.turret_basic_base = pg.image.load(r'assets\shakers\Red\Towers\base.png').convert_alpha()
        self.turret_basic_base = pg.transform.scale_by(self.turret_basic_base, 0.5)
        self.turret_basic_sound = pg.mixer.Sound(r'assets\sounds\tock.wav')

        # Load laser turret assets
        self.turret_laser_sprite_sheets = []
        for x in range(1, TURRET_DATA_LASER_GUN.get('constants').get('levels') + 1):
            self.turret_sheet = pg.image.load(rf'assets\shakers\Blue\Weapons\turret_02_mk{x}.png').convert_alpha()
            self.turret_laser_sprite_sheets.append(self.turret_sheet)
        self.turret_laser_base = pg.image.load(r'assets\shakers\Blue\Towers\base.png').convert_alpha()
        self.turret_laser_base = pg.transform.scale_by(self.turret_laser_base, 0.5)
        self.turret_laser_sound = pg.mixer.Sound(r'assets\sounds\laser_fire.wav')

    def create_turret(self, turret_type, x, y):
        new_turret = None
        if turret_type == "basic":
            new_turret = Turret(x, y, TURRET_DATA_BASIC_GUN)
            new_turret.sprite_sheets = self.turret_basic_sprite_sheets
            new_turret.base_image = self.turret_basic_base
            new_turret.gun_sound = self.turret_basic_sound

        elif turret_type == "laser":
            new_turret = Turret(x, y, TURRET_DATA_LASER_GUN)
            new_turret.sprite_sheets = self.turret_laser_sprite_sheets
            new_turret.base_image = self.turret_laser_base
            new_turret.gun_sound = self.turret_laser_sound
        else:
            raise ValueError(f"Unknown turret type: {turret_type}")

        new_turret.original_base_image = new_turret.base_image
        new_turret.base_image_rect = new_turret.base_image.get_rect()
        new_turret.animation_list = new_turret.load_images(new_turret.sprite_sheets[new_turret.upgrade_level - 1])
        new_turret.original_image = new_turret.animation_list[new_turret.frame_index]
        new_turret.image = pg.transform.rotate(new_turret.original_image, new_turret.angle)
        new_turret.rect = new_turret.image.get_rect()
        new_turret.rect.center = (new_turret.x, new_turret.y)
        new_turret.range_rect.center = new_turret.rect.center
        new_turret.base_image_rect.center = new_turret.rect.center

        return new_turret

    def get_turret_costs(self, turret_type):
        if turret_type == "basic":
            return TURRET_DATA_BASIC_GUN.get('constants').get('buy_cost')
        if turret_type == "laser":
            return TURRET_DATA_LASER_GUN.get('constants').get('buy_cost')

        raise ValueError(f"Unknown turret type: {turret_type}")
