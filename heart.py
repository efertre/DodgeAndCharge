
import constants

class Heart:
    def __init__(self, x, y, images, lives):
        self.images = images  # Lista de imágenes para la animación de los corazones
        self.lives = lives    # Número de vidas inicial del jugador
        self.x = x            # Posición inicial en X
        self.y = y            # Posición inicial en Y
        self.animation_index = 0       # Índice para la imagen actual de la animación
        self.animation_counter = 0      # Contador de tiempo para animación

    def update(self):
        # Incrementar el contador de animación
        self.animation_counter += constants.ANIMATION_SPEED
        if self.animation_counter >= 1:
            # Cambiar al siguiente fotograma en la animación
            self.animation_index = (self.animation_index + 1) % len(self.images)
            self.animation_counter = 0  # Reiniciar el contador

    def draw(self, screen):
        # Dibujar tantos corazones como vidas tenga el jugador
        for i in range(self.lives):
            # Calcular la posición de cada corazón
            heart_x = self.x + i * (constants.HEART_SIZE[0] + 5)
            # Seleccionar el fotograma actual para la animación
            heart_image = self.images[self.animation_index]
            # Dibujar el fotograma en pantalla
            screen.blit(heart_image, (heart_x, self.y))
