# camera.py
import pygame

import constants


class Camera:
    def __init__(self, width, height):
        self.camera_rect = pygame.Rect(0, 0, width, height)  # Área de la cámara
        self.width = width
        self.height = height

    def apply(self, obj):
        """ Ajusta la posición de cualquier objeto en función de la cámara """
        # Verificar si el objeto tiene un atributo 'rect'; si no, asumimos que es un Rect directamente
        # Si el objeto es un rectangulo o el objeto pasado contiene el atributo rectangulo
        rect = obj.rect if hasattr(obj, 'rect') else obj
        return rect.move(self.camera_rect.topleft)

    def update(self, target):
        """ Centra la cámara en el objetivo (personaje) """
        x = -target.rect.centerx + int(constants.WIDTH / 2)
        y = -target.rect.centery + int(constants.HEIGHT / 2)

        # Limita la cámara a los bordes del nivel
        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - constants.WIDTH), x)
        y = max(-(self.height - constants.HEIGHT), y)

        self.camera_rect = pygame.Rect(x, y, self.width, self.height)
