# character.py
import pygame
import constants
from utils import Utils

class Character:
    def __init__(self, center_position):
        self.animations = {
            "up": Utils.load_animation(constants.CHARACTER_UP_PATH, 4, constants.CHARACTER_SIZE),
            "down": Utils.load_animation(constants.CHARACTER_DOWN_PATH, 6, constants.CHARACTER_SIZE),
            "left": Utils.load_animation(constants.CHARACTER_LEFT_PATH, 8, constants.CHARACTER_SIZE),
            "right": Utils.load_animation(constants.CHARACTER_RIGHT_PATH, 8, constants.CHARACTER_SIZE)
        }
        self.current_direction = self.animations["down"]
        self.rect = self.current_direction[0].get_rect(center=center_position)
        self.animation_index = 0
        self.animation_counter = 0

    def move(self, keys):
        moving = False
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.rect.top > 0:
            self.rect.move_ip(0, -constants.CHARACTER_SPEED)
            self.set_direction("up")
            moving = True
        elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.rect.bottom < constants.HEIGHT:
            self.rect.move_ip(0, constants.CHARACTER_SPEED)
            self.set_direction("down")
            moving = True
        elif (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.left > 0:
            self.rect.move_ip(-constants.CHARACTER_SPEED, 0)
            self.set_direction("left")
            moving = True
        elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.right < constants.WIDTH:
            self.rect.move_ip(constants.CHARACTER_SPEED, 0)
            self.set_direction("right")
            moving = True

        self.animate(moving)

    def set_direction(self, direction):
        if self.current_direction != self.animations[direction]:
            self.current_direction = self.animations[direction]
            self.animation_index = 0

    def animate(self, moving):
        if moving:
            self.animation_counter += constants.ANIMATION_SPEED
            if self.animation_counter >= 1:
                self.animation_index = (self.animation_index + 1) % len(self.current_direction)
                self.animation_counter = 0
        else:
            self.animation_index = 0

    def draw(self, surface):
        surface.blit(self.current_direction[self.animation_index], self.rect)
