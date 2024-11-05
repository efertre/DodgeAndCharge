# projectile.py
import pygame
import constants
import math


class Projectile:
    def __init__(self, start_pos, target_pos):
        # Cargar y escalar imagen del proyectil
        self.image = pygame.transform.scale(pygame.image.load(constants.PROJECTILE_IMG_PATH), constants.PROJECTILE_SIZE)
        self.rect = self.image.get_rect(center=start_pos)

        # Calcular la dirección normalizada hacia el objetivo
        dx, dy = target_pos[0] - start_pos[0], target_pos[1] - start_pos[1]
        distance = math.hypot(dx, dy)
        self.direction = (dx / distance, dy / distance) if distance != 0 else (0, 0)

    def move(self):
        # Mover el proyectil en la dirección calculada
        self.rect.move_ip(self.direction[0] * constants.PROJECTILE_SPEED,
                          self.direction[1] * constants.PROJECTILE_SPEED)

    def draw(self, surface):
        # Dibujar el proyectil en la pantalla
        surface.blit(self.image, self.rect)

    def is_off_screen(self):
        # Verificar si el proyectil sale de la pantalla
        return (self.rect.bottom < 0 or self.rect.top > constants.HEIGHT or
                self.rect.left < 0 or self.rect.right > constants.WIDTH)
