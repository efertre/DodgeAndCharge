import random
import pygame
import constants

class Camera:
    def __init__(self, width, height):
        self.camera_rect = pygame.Rect(0, 0, width, height)  # Área de la cámara
        self.width = width
        self.height = height

        # Variables para el temblor
        self.shaking = False
        self.shake_duration = 0
        self.shake_intensity = 5  # Intensidad del temblor
        self.shake_offset = pygame.Vector2(0, 0)  # Desplazamiento del temblor

    def start_shake(self, duration, intensity=5):
        """ Inicia el efecto de temblor """
        self.shaking = True
        self.shake_duration = duration
        self.shake_intensity = intensity

    def update(self, target):
        """ Centra la cámara en el objetivo (personaje) y aplica temblor si está activo """
        x = -target.rect.centerx + int(constants.WIDTH / 2)
        y = -target.rect.centery + int(constants.HEIGHT / 2)

        # Limita la cámara a los bordes del nivel
        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - constants.WIDTH), x)
        y = max(-(self.height - constants.HEIGHT), y)

        # Actualiza el temblor, la cámara se mueve de
        # forma aleatoria dentro de los límites establecidos por la intensidad.
        if self.shaking:
            self.shake_offset.x = random.randint(-self.shake_intensity, self.shake_intensity)
            self.shake_offset.y = random.randint(-self.shake_intensity, self.shake_intensity)
            self.shake_duration -= 1
            if self.shake_duration <= 0:
                self.shaking = False
                self.shake_offset = pygame.Vector2(0, 0)

        # Ajusta la posición de la cámara aplicando el temblor
        self.camera_rect = pygame.Rect(x + self.shake_offset.x, y + self.shake_offset.y, self.width, self.height)

    def apply(self, obj):
        """ Ajusta la posición de cualquier objeto en función de la cámara """
        rect = obj.rect if hasattr(obj, 'rect') else obj
        return rect.move(self.camera_rect.topleft)
