import pygame
import constants
import random

# Generadores de parámetros aleatorios
def random_position_generator(width, height, rect_width, rect_height, player_rect, min_distance):
    """Generador para posiciones aleatorias dentro de los límites de la pantalla, evitando cercanía al jugador."""
    while True:
        x = random.randint(0, width - rect_width)
        y = random.randint(0, height - rect_height)
        new_position = pygame.Rect(x, y, rect_width, rect_height)

        # Verificar si la nueva posición está a una distancia segura del jugador
        if new_position.colliderect(player_rect.inflate(min_distance, min_distance)):
            continue  # Si colisiona, volver a intentar

        yield (x, y)

def random_speed_generator(speed_range):
    """Generador para velocidades aleatorias en un rango determinado."""
    while True:
        yield random.choice([-1, 1]) * random.randint(*speed_range)

class Ball:
    position_gen = None
    speed_gen = random_speed_generator(constants.BALL_SPEED_RANGE)

    def __init__(self, player_rect):
        # Cargar y escalar la imagen de la bola
        self.image = pygame.transform.scale(pygame.image.load(constants.BALL_IMG_PATH), constants.BALL_SIZE)

        # Inicializar el rectángulo de la bola basado en su imagen
        self.rect = self.image.get_rect()

        # Inicializar el generador de posiciones con la posición del jugador
        self.position_gen = random_position_generator(constants.WIDTH, constants.HEIGHT, constants.BALL_SIZE[0], constants.BALL_SIZE[1], player_rect, min_distance=200)

        # Establecer posición inicial utilizando el generador
        self.rect.topleft = next(self.position_gen)

        # Establecer velocidad inicial utilizando el generador
        self.speed = [next(self.speed_gen), next(self.speed_gen)]

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
