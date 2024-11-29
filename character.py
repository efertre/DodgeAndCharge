import pygame
import constants
from constants import MOVEMENT_MARGIN_LEFT
from utils import Utils

class Character:
    def __init__(self, center_position, width, height):
        # Recibe los nuevos parámetros WIDTH y HEIGHT
        self.width = width
        self.height = height
        self.animations = {
            "up": Utils.load_animation(constants.CHARACTER_UP_PATH, 4, constants.CHARACTER_SIZE),
            "down": Utils.load_animation(constants.CHARACTER_DOWN_PATH, 6, constants.CHARACTER_SIZE),
            "left": Utils.load_animation(constants.CHARACTER_LEFT_PATH, 8, constants.CHARACTER_SIZE),
            "right": Utils.load_animation(constants.CHARACTER_RIGHT_PATH, 8, constants.CHARACTER_SIZE),
            "death": Utils.load_animation(constants.CHARACTER_DEATH_PATH, 8, constants.CHARACTER_SIZE)
        }
        self.current_direction = self.animations["down"]
        self.rect = self.current_direction[0].get_rect(center=center_position)
        self.animation_index = 0
        self.animation_counter = 0
        self.hearts = 3
        self.is_dead = False

    def move(self, keys):
        if self.is_dead:
            return  # No permitir movimiento si está muerto

        moving = False
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            if self.rect.top > 0 + constants.MOVEMENT_MARGIN_TOP:
                self.rect.move_ip(0, -constants.CHARACTER_SPEED)
                self.set_direction("up")
                moving = True
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if self.rect.bottom < constants.HEIGHT + constants.MOVEMENT_MARGIN_BOTTOM:
                self.rect.move_ip(0, constants.CHARACTER_SPEED)
                self.set_direction("down")
                moving = True
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if self.rect.left > 0 + constants.MOVEMENT_MARGIN_LEFT:
                self.rect.move_ip(-constants.CHARACTER_SPEED, 0)
                self.set_direction("left")
                moving = True
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if self.rect.right < constants.WIDTH + constants.MOVEMENT_MARGIN_RIGHT:
                self.rect.move_ip(constants.CHARACTER_SPEED, 0)
                self.set_direction("right")
                moving = True

        self.animate(moving)

    def set_direction(self, direction):
        """ Cambia la dirección y reinicia el índice de animación si cambia la dirección. """
        if self.current_direction != self.animations[direction]:
            self.current_direction = self.animations[direction]
            self.animation_index = 0

    def animate(self, moving):
        """ Controla la animación basada en si el personaje se está moviendo. """

        if self.is_dead:
            self.animation_counter += constants.ANIMATION_SPEED
            print(f"MUERTO: {self.animation_counter}")
            if self.animation_counter >= 1:
                self.animation_index += 1
                self.animation_counter = 0
            else:
                self.animation_index = 0
                return True

        if moving:
            self.animation_counter += constants.ANIMATION_SPEED
            print(self.animation_counter)
            if self.animation_counter >= 1:
                self.animation_index = (self.animation_index + 1) % len(self.current_direction)
                self.animation_counter = 0
        else:
            self.animation_index = 0
        return False



    def draw(self, surface, camera):
        """ Dibuja el personaje en la superficie y ajusta la posición con la cámara. """
        adjusted_position = camera.apply(self.rect)

        surface.blit(self.current_direction[self.animation_index], adjusted_position)


