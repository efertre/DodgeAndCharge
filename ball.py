# ball.py
import pygame
import random
import constants


class Ball:
    def __init__(self):
        # Cargar y escalar la imagen de la bola
        self.image = pygame.transform.scale(pygame.image.load(constants.BALL_IMG_PATH), constants.BALL_SIZE)

        # Inicializar el rectángulo de la bola basado en su imagen
        self.rect = self.image.get_rect()

        # Establecer posición inicial aleatoria
        self.rect.topleft = (
            random.randint(0, constants.WIDTH - self.rect.width),
            random.randint(0, constants.HEIGHT - self.rect.height)
        )

        # Establecer velocidad aleatoria
        self.speed = [
            random.choice([-1, 1]) * random.randint(*constants.BALL_SPEED_RANGE),
            random.choice([-1, 1]) * random.randint(*constants.BALL_SPEED_RANGE)
        ]

    def move(self):
        # Mover la bola y hacer que rebote en los bordes de la pantalla
        self.rect.move_ip(*self.speed)

        if self.rect.left < 0 or self.rect.right > constants.WIDTH:
            self.speed[0] = -self.speed[0]
        if self.rect.top < 0 or self.rect.bottom > constants.HEIGHT:
            self.speed[1] = -self.speed[1]

    def draw(self, surface):
        # Dibujar la bola en la pantalla
        surface.blit(self.image, self.rect)
