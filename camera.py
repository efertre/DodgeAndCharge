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
        """
        Ajusta la posición de cualquier objeto en función de la posición de la cámara.
        Esto permite que los objetos en el mapa se muestren correctamente en la ventana de visualización
        según el desplazamiento actual de la cámara.
        """

        # Verifica si el objeto tiene un atributo 'rect' (lo cual es común para sprites y objetos de juego).
        # Si lo tiene, utilizamos su rectángulo; si no, asumimos que 'obj' ya es un rectángulo (pygame.Rect).
        rect = obj.rect if hasattr(obj, 'rect') else obj

        # Ajusta las coordenadas del rectángulo del objeto según la posición de la cámara.
        # 'self.camera_rect.topleft' representa el desplazamiento de la cámara desde el origen del mapa.
        # 'rect.move()' devuelve un nuevo rectángulo desplazado.
        return rect.move(self.camera_rect.topleft)

    def reset(self):
        """Reinicia la cámara a su posición inicial"""
        self.camera_rect = pygame.Rect(0, 0, self.width, self.height)  # Resetear la posición de la cámara
        self.shaking = False  # Desactivar el temblor
        self.shake_duration = 0  # Resetear la duración del temblor
        self.shake_intensity = 5  # Intensidad predeterminada
        self.shake_offset = pygame.Vector2(0, 0)  # Resetear el desplazamiento del temblor

