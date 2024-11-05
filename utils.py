import pygame

class Utils:
    @staticmethod
    def load_animation(path, num_images, scale):
        """Carga y escala una serie de imágenes para la animación."""
        images = []
        for i in range(1, num_images + 1):
            img = pygame.image.load(f"{path}{i}.png")
            images.append(pygame.transform.scale(img, scale))
        return images
