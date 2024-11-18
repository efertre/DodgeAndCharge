import pygame
import constants
import random
from utils import Utils

# Generadores de parámetros aleatorios
def random_position_generator(width, height, rect_width, rect_height, player_rect, min_distance):
    """Generador para posiciones aleatorias dentro de los límites de la pantalla, evitando cercanía al jugador."""
    while True:
        x = random.randint(constants.MOVEMENT_MARGIN_LEFT, width - rect_width + constants.MOVEMENT_MARGIN_RIGHT)
        y = random.randint(constants.MOVEMENT_MARGIN_TOP, height - rect_height + constants.MOVEMENT_MARGIN_BOTTOM)

        new_position = pygame.Rect(x, y, rect_width, rect_height)

        # Verificar si la nueva posición está a una distancia segura del jugador
        if new_position.colliderect(player_rect.inflate(min_distance, min_distance)):
            continue  # Si colisiona, volver a intentar

        yield (x, y)

def random_speed_generator(speed_range):
    """Generador para velocidades aleatorias en un rango determinado."""
    while True:
        yield random.choice([-1, 1]) * random.randint(*speed_range)

class Slime:
    position_gen = None
    speed_gen = random_speed_generator(constants.BALL_SPEED_RANGE)

    def __init__(self, player_rect):
        # Cargar y escalar la imagen de la bola
        self.animations = Utils.load_animation(constants.SLIME_IMG_PATH, 8, constants.SLIME_SIZE)
        self.animation_index = 0
        self.animation_counter = 0
        self.flipped = False

        # Inicializar el rectángulo de la bola basado en su imagen
        self.rect = self.animations[0].get_rect()

        # Inicializar el generador de posiciones con la posición del jugador
        self.position_gen = random_position_generator(constants.WIDTH, constants.HEIGHT, constants.SLIME_SIZE[0],
                                                      constants.SLIME_SIZE[1], player_rect, min_distance=200)

        # Establecer posición inicial utilizando el generador
        self.rect.topleft = next(self.position_gen)

        # Establecer velocidad inicial utilizando el generador
        self.speed = [next(self.speed_gen), next(self.speed_gen)]

    def animate(self, moving):
        """ Controla la animación. """
        if moving:
            self.animation_counter += constants.ANIMATION_SPEED
            if self.animation_counter >= 1:
                self.animation_index = (self.animation_index + 1) % len(self.animations)
                self.animation_counter = 0
        else:
            self.animation_index = 0

    def move(self):
        # Mover la bola y hacer que rebote en los bordes de la pantalla
        self.rect.move_ip(*self.speed)
        moving = True
        if self.rect.left < 0 + constants.MOVEMENT_MARGIN_LEFT or self.rect.right > constants.WIDTH + constants.MOVEMENT_MARGIN_RIGHT:
            self.speed[0] = -self.speed[0]
            self.flipped = not self.flipped

        if self.rect.top < 0 + constants.MOVEMENT_MARGIN_TOP or self.rect.bottom > constants.HEIGHT + constants.MOVEMENT_MARGIN_BOTTOM:
            self.speed[1] = -self.speed[1]

        self.animate(moving)

    def draw(self, surface):
        # Dibujar el slime con la orientación actual
        frame = self.animations[self.animation_index]
        if self.flipped:
            frame = pygame.transform.flip(frame, True, False)  # Voltear horizontalmente
        surface.blit(frame, self.rect)
