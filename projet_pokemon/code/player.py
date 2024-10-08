import pygame

from entity import Entity
from keylistener import KeyListener
from screen import Screen
from switch import Switch


class Player(Entity):
    def __init__(self, keylistener: KeyListener, screen: Screen, x: int, y: int):
        super().__init__(keylistener, screen, x, y)
        self.current_image_index = None
        self.in_pokeball_mode = False
        self.pokedollars: int = 0
        self.on_bike: bool = False
        self.is_wheeling: bool = False
        self.life: int = 40
        self.spritesheet_bike: pygame.image = pygame.image.load("../assets/sprite/hero_01_red_m_cycle_roll.png")
        self.spritesheet_whelling: pygame.image = pygame.image.load("../assets/sprite/hero_01_red_m_cycle_wheel.png")
        self.spritesheet_poke = pygame.image.load("../assets/sprite/hero_01_red_m_pokecenter.png")

        self.switchs: list[Switch] | None = None
        self.collisions: list[pygame.Rect] | None = None
        self.change_map: Switch | None = None

    def update(self) -> None:
        self.check_input()
        self.check_move()
        super().update()

    def check_move(self) -> None:
        if self.animation_walk is False:
            temp_hitbox = self.hitbox.copy()
            if self.keylistener.key_pressed(pygame.K_q):
                temp_hitbox.x -= 16
                if not self.check_collisions(temp_hitbox):
                    self.check_collisions_switchs(temp_hitbox)
                    self.move_left()
                else:
                    self.direction = "left"
            elif self.keylistener.key_pressed(pygame.K_d):
                temp_hitbox.x += 16
                if not self.check_collisions(temp_hitbox):
                    self.check_collisions_switchs(temp_hitbox)
                    self.move_right()
                else:
                    self.direction = "right"
            elif self.keylistener.key_pressed(pygame.K_z):
                temp_hitbox.y -= 16
                if not self.check_collisions(temp_hitbox):
                    self.check_collisions_switchs(temp_hitbox)
                    self.move_up()
                else:
                    self.direction = "up"
            elif self.keylistener.key_pressed(pygame.K_s):
                temp_hitbox.y += 16
                if not self.check_collisions(temp_hitbox):
                    self.check_collisions_switchs(temp_hitbox)
                    self.move_down()
                else:
                    self.direction = "down"

    def add_switchs(self, switchs: list[Switch]):
        self.switchs = switchs

    def check_collisions_switchs(self, temp_hitbox):
        if self.switchs:
            for switch in self.switchs:
                if switch.check_collision(temp_hitbox):
                    self.change_map = switch
        return None

    def add_collisions(self, collisions):
        self.collisions = collisions

    def check_collisions(self, temp_hitbox: pygame.Rect):
        for collision in self.collisions:
            if temp_hitbox.colliderect(collision):
                return True
        return False

    def check_input(self):
        if self.keylistener.key_pressed(pygame.K_b):
            self.switch_bike()
        if self.keylistener.key_pressed(pygame.K_a) and self.on_bike:
            self.switch_wheeling()
        if self.keylistener.key_pressed(pygame.K_e) and not self.on_bike:
            if self.in_pokeball_mode:
                self.switch_walk()
            else:
                self.switch_watch_pokeball()

    def switch_walk(self):
        self.speed = 1
        self.in_pokeball_mode = False
        self.all_images = self.get_all_images(self.spritesheet)
        self.keylistener.remove_key(pygame.K_e)

    def switch_wheeling(self):
        if self.on_bike and not self.is_wheeling:
            self.speed = 4
            self.is_wheeling = True
            self.all_images = self.get_all_images(self.spritesheet_whelling)
        else:
            self.is_wheeling = False
            self.all_images = self.get_all_images(self.spritesheet_bike)
        self.keylistener.remove_key(pygame.K_a)

    def switch_bike(self, desactive=False):
        if not self.on_bike and not desactive:
            self.on_bike = True
            self.speed = 4
            self.all_images = self.get_all_images(self.spritesheet_bike)
        else:
            self.speed = 1
            self.on_bike = False
            self.all_images = self.get_all_images(self.spritesheet)
        self.keylistener.remove_key(pygame.K_b)

    def switch_watch_pokeball(self):
        if not self.on_bike:
            self.speed = 0
            all_images_dict = self.get_all_images(self.spritesheet_poke)
            self.in_pokeball_mode = True
            if 'right' in all_images_dict and all_images_dict['right']:
                self.all_images = {'right': [all_images_dict['right'][3]]}
                self.direction = 'right'
                self.index_image = 0

        else:
            self.in_pokeball_mode = False
            self.all_images = self.get_all_images(self.spritesheet)

        self.keylistener.remove_key(pygame.K_e)