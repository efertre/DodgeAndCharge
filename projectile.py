# projectile.py
from turtledemo.penrose import start

import pygame
import constants

class Projectile:
    def __init__(self, start_pos, target_pos, dir):
        # Cargar y escalar imagen del proyectil
        self.image = pygame.transform.scale(pygame.image.load(constants.PROJECTILE_IMG_PATH), constants.PROJECTILE_SIZE)
        # El proyectil se coloca en la posición central del jugador
        self.rect = self.image.get_rect(center=start_pos)

        # Calcular la dirección normalizada hacia el objetivo, desde el centro del mapa a la dirección del cursor
        self.direction = (target_pos - dir).normalize()

    def move(self):
        # Mover el proyectil en la dirección calculada
        self.rect.move_ip(self.direction[0] * constants.PROJECTILE_SPEED,
                          self.direction[1] * constants.PROJECTILE_SPEED)

    def draw(self, surface):
        # Dibujar el proyectil en la pantalla
        surface.blit(self.image, self.rect)

    def is_off_screen(self):
        # Verificar si el proyectil sale de la pantalla
        # Esto se hace verificando si el proyectil está fuera de los márgenes
        return (self.rect.bottom > constants.HEIGHT + constants.MOVEMENT_MARGIN_BOTTOM or
                self.rect.top < constants.MOVEMENT_MARGIN_TOP or
                self.rect.left < constants.MOVEMENT_MARGIN_LEFT or
                self.rect.right > constants.WIDTH + constants.MOVEMENT_MARGIN_RIGHT)
