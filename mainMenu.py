# mainMenu.py
import pygame
import constants

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.buttons = ["Jugar", "Opciones", "Salir"]
        self.selected_index = 0  # Índice del botón seleccionado
        self.title_font = pygame.font.Font(constants.FONT_PATH, constants.TITLE_FONT_SIZE)
        self.subtitle_font = pygame.font.Font(constants.FONT_PATH, constants.SUBTITLE_FONT_SIZE)
        self.button_font = pygame.font.Font(constants.FONT_PATH, constants.FONT_SIZE)
        self.title = "Dodge & Charge"
        self.subtitle = "creado por efertre"

        # Cargar el fondo para el menú
        try:
            self.background_img = pygame.image.load(constants.MAIN_MENU_BACKGROUND_IMG_PATH).convert()
            self.bg_width = self.background_img.get_width()
            self.bg_x = 0  # Posición inicial del fondo
            self.bg_speed = 1  # Velocidad de desplazamiento
        except pygame.error:
            print("No se pudo cargar la imagen de fondo del menú.")

    def draw(self):
        # Dibujar fondo animado
        self.screen.blit(self.background_img, (self.bg_x, 0))
        self.screen.blit(self.background_img, (self.bg_x - self.bg_width, 0))

        # Actualizar la posición del fondo para que se desplace
        self.bg_x += self.bg_speed
        if self.bg_x >= self.bg_width:
            self.bg_x = 0  # Reiniciar la posición para hacer el bucle

        # Dibujar título
        title_surf = self.title_font.render(self.title, True, constants.WHITE)
        title_rect = title_surf.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT // 4))
        self.screen.blit(title_surf, title_rect)

        # Dibujar subtítulo
        subtitle_surf = self.subtitle_font.render(self.subtitle, True, constants.WHITE)
        subtitle_rect = subtitle_surf.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT // 4 + 40))
        self.screen.blit(subtitle_surf, subtitle_rect)

        # Dibujar los botones
        for index, button_text in enumerate(self.buttons):
            color = constants.YELLOW if index == self.selected_index else constants.WHITE
            button_surf = self.button_font.render(button_text, True, color)
            button_rect = button_surf.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT // 2 + index * 40))
            self.screen.blit(button_surf, button_rect)

    def handle_mouse(self, mouse_pos):
        # Detectar si el mouse está sobre algún botón
        for index, button_text in enumerate(self.buttons):
            button_rect = self.button_font.render(button_text, True, constants.WHITE).get_rect(
                center=(constants.WIDTH // 2, constants.HEIGHT // 2 + index * 40))
            if button_rect.collidepoint(mouse_pos):
                self.selected_index = index
                break

    def handle_click(self):
        # Retorna el nombre del botón seleccionado cuando se hace clic
        return self.buttons[self.selected_index]

    def handle_keys(self, event):
        # Navegación con teclas
        if event.key in (pygame.K_DOWN, pygame.K_s):
            self.selected_index = (self.selected_index + 1) % len(self.buttons)
        elif event.key in (pygame.K_UP, pygame.K_w):
            self.selected_index = (self.selected_index - 1) % len(self.buttons)
        elif event.key == pygame.K_RETURN:
            return self.buttons[self.selected_index]  # Retorna el botón seleccionado cuando presionas ENTER
