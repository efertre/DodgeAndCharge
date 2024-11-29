import json
import os
import pygame
import constants
global_music_volume = 0
global_sfx_volume = 0

class OptionsMenu:

    def __init__(self, screen):
        self.screen = screen
        self.title_font = pygame.font.Font(constants.FONT_PATH, constants.TITLE_FONT_SIZE)
        self.font = pygame.font.Font(constants.FONT_PATH, constants.FONT_SIZE)
        self.title = "Opciones de Juego"
        self.options = ["Volumen Música", "Volumen Efectos", "Volver"]
        self.selected_index = 0
        self.music_volume = 50
        self.sfx_volume = 50

        # Leer configuración guardada
        self.load_settings()

        # Título
        self.title_surf = self.title_font.render(self.title, True, constants.WHITE)
        self.title_rect = self.title_surf.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT // 5))

        self.spacing_y = 100
        self.start_y = self.title_rect.bottom + 80

        # Cargar sonidos
        self.hover_sound = pygame.mixer.Sound("sound/hover_sound.ogg")

        # Fondo del menú
        try:
            self.background_img = pygame.image.load(constants.STATS_MENU_BACKGROUND_IMG_PATH).convert()
            self.bg_width = self.background_img.get_width()
        except pygame.error:
            print("No se pudo cargar la imagen de fondo del menú de opciones.")

        # Aplicar volumen inicial
        pygame.mixer.music.set_volume(self.music_volume / 100)
        self.hover_sound.set_volume(self.sfx_volume / 100)


        # Variables para sliders
        self.slider_width = 200
        self.slider_height = 10
        self.slider_color = constants.WHITE
        self.knob_color = constants.YELLOW
        self.dragging_music = False
        self.dragging_effects = False

    def draw(self):
        self.draw_animated_bg()

        # Dibujar el título
        self.screen.blit(self.title_surf, self.title_rect)

        # Dibujar las opciones del menú
        for index, option_text in enumerate(self.options):
            color = constants.YELLOW if self.selected_index == index else constants.WHITE
            option_surf = self.font.render(option_text, True, color)
            option_rect = option_surf.get_rect(center=(constants.WIDTH // 2, self.start_y + self.spacing_y * index))
            self.screen.blit(option_surf, option_rect)

            # Dibujar sliders para los volúmenes
            if option_text == "Volumen Música":
                self.draw_slider(self.music_volume, self.start_y + self.spacing_y * index + 50)
            elif option_text == "Volumen Efectos":
                self.draw_slider(self.sfx_volume, self.start_y + self.spacing_y * index + 50)

    def draw_slider(self, value, y_position):
        """Dibuja un slider para ajustar el volumen."""
        x_position = constants.WIDTH // 2 - self.slider_width // 2
        pygame.draw.rect(self.screen, self.slider_color, (x_position, y_position, self.slider_width, self.slider_height))
        knob_x = x_position + (value / 100) * self.slider_width
        knob_y = y_position + self.slider_height // 2
        pygame.draw.circle(self.screen, self.knob_color, (int(knob_x), int(knob_y)), 10)

    def draw_animated_bg(self):
        self.screen.blit(self.background_img, (constants.BACKGROUND_POSITION, 0))
        self.screen.blit(self.background_img, (constants.BACKGROUND_POSITION - self.bg_width, 0))
        constants.BACKGROUND_POSITION += constants.BACKGROUND_SPEED
        if constants.BACKGROUND_POSITION >= self.bg_width:
            constants.BACKGROUND_POSITION = 0

    def handle_keys(self, event):
        last_index = self.selected_index
        if event.key in (pygame.K_DOWN, pygame.K_s):
            self.selected_index = (self.selected_index + 1) % len(self.options)
        elif event.key in (pygame.K_UP, pygame.K_w):
            self.selected_index = (self.selected_index - 1) % len(self.options)
        elif event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
            self.save_settings()
            return self.options[self.selected_index]
        elif event.key == pygame.K_RIGHT:
            self.adjust_volume(1)
        elif event.key == pygame.K_LEFT:
            self.adjust_volume(-1)

        if last_index != self.selected_index:
            self.hover_sound.play()

    def handle_mouse(self, mouse_pos):
        """Detectar clic y arrastre para los sliders y la selección de botones."""
        global global_music_volume, global_sfx_volume
        global_sfx_volume = self.sfx_volume

        mouse_x, mouse_y = mouse_pos  # Desempaquetar las coordenadas del mouse
        last_index = self.selected_index  # Recordar el último índice seleccionado
        x_position = constants.WIDTH // 2 - self.slider_width // 2  # Posición del slider

        # Detectar interacción con el slider de música
        if self.start_y + self.spacing_y * 0.5 <= mouse_y <= self.start_y + self.spacing_y * 0.5 + 30:
            if pygame.mouse.get_pressed()[0]:  # Verificar si el botón izquierdo está presionado
                self.dragging_music = True
            elif not pygame.mouse.get_pressed()[0]:  # Soltar el arrastre
                self.dragging_music = False

            if self.dragging_music:
                global_music_volume = int((mouse_x - x_position) / self.slider_width * 100)
                global_music_volume = min(max(global_music_volume, 0), 100)
                pygame.mixer.music.set_volume(global_music_volume / 100)

        # Detectar interacción con el slider de efectos
        elif self.start_y + self.spacing_y * 1.5 <= mouse_y <= self.start_y + self.spacing_y * 1.5 + 30:
            if pygame.mouse.get_pressed()[0]:
                self.dragging_effects = True
            elif not pygame.mouse.get_pressed()[0]:
                self.dragging_effects = False

            if self.dragging_effects:
                global_sfx_volume = int((mouse_x - x_position) / self.slider_width * 100)
                global_sfx_volume = min(max(global_sfx_volume, 0), 100)
                self.hover_sound.set_volume(global_sfx_volume / 100)

        # Detectar si el mouse está sobre algún botón (de las opciones)
        for index, option_text in enumerate(self.options):
            option_rect = self.font.render(option_text, True, constants.WHITE).get_rect(
                center=(constants.WIDTH // 2, self.start_y + self.spacing_y * index))

            # Verificar si el ratón está sobre el botón
            if option_rect.collidepoint(mouse_pos):
                self.selected_index = index  # Actualizar el índice seleccionado

                # Solo reproducir el sonido si el mouse ha cambiado de botón
                if last_index != self.selected_index:
                    self.hover_sound.set_volume(self.sfx_volume / 100)
                    self.hover_sound.play()
                    self.sfx_volume = global_sfx_volume
                    self.music_volume = global_music_volume
                    self.save_settings()
                return self.options[index]  # Retorna el texto del botón sobre el que está el ratón

        self.sfx_volume = global_sfx_volume
        self.music_volume = global_music_volume
        self.save_settings()
        return None  # Si no hay interacción con ningún botón

    def adjust_volume(self, change):
        global global_music_volume, global_sfx_volume
        global_sfx_volume = self.sfx_volume

        global_music_volume = self.music_volume
        if self.options[self.selected_index] == "Volumen Música":
            global_music_volume = min(100, max(0, global_music_volume + change * 5))
            pygame.mixer.music.set_volume(global_music_volume / 100)
        elif self.options[self.selected_index] == "Volumen Efectos":
            global_sfx_volume = min(100, max(0, global_sfx_volume + change * 5))
            self.hover_sound.set_volume(global_sfx_volume / 100)

        self.sfx_volume = global_sfx_volume
        self.music_volume = global_music_volume

    def save_settings(self):
        """Guardar configuración en un archivo JSON."""
        settings = {
            "music_volume": self.music_volume,
            "sfx_volume": self.sfx_volume
        }
        with open("settings.json", "w") as f:
            json.dump(settings, f)

    def load_settings(self):
        """Cargar configuración desde un archivo JSON."""
        if os.path.exists("settings.json"):
            with open("settings.json", "r") as f:
                settings = json.load(f)
                self.music_volume = settings.get("music_volume", 50)

                self.sfx_volume = settings.get("sfx_volume", 50)

            global global_sfx_volume, global_music_volume

            global_sfx_volume = self.sfx_volume
            global_music_volume = self.music_volume