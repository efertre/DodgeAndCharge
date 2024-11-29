import pygame

import optionsMenu
from utils import load_stats, reset_stats  # Supone que tienes una función reset_statistics en utils
import constants

class StatsMenu:
    def __init__(self, screen):
        self.screen = screen
        self.title_font = pygame.font.Font(constants.FONT_PATH, constants.TITLE_FONT_SIZE)
        self.font = pygame.font.Font(constants.FONT_PATH, constants.FONT_SIZE)
        self.title = "Estadísticas de Juego"
        self.options = ["Volver", "Borrar datos"]
        self.selected_index = 0  # Índice de opción seleccionada
        # Título
        self.title_surf = self.title_font.render(self.title, True, constants.WHITE)
        self.title_rect = self.title_surf.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT // 5))
        # Posiciones de las estadísticas
        self.spacing_y = 50 #
        self.start_y = self.title_rect.bottom + 20
        # Cargar sonidos
        self.hover_sound = pygame.mixer.Sound("sound/hover_sound.ogg")
        self.hover_sound.set_volume(optionsMenu.global_sfx_volume / 100)

        # Cargar el fondo para el menú
        try:
            self.background_img = pygame.image.load(constants.STATS_MENU_BACKGROUND_IMG_PATH).convert()
            self.bg_width = self.background_img.get_width()
        except pygame.error:
            print("No se pudo cargar la imagen de fondo del menú estadísticas.")

    # Metodo para dibujar todos los componentes del menu de estadisticas
    def draw(self):
        self.draw_animated_bg()

        # Dibujar el título
        self.screen.blit(self.title_surf, self.title_rect)

        avg_score_text, best_score_text, games_played_text, total_score_text = self.load_stats_from_utils()

        self.draw_stats(avg_score_text, best_score_text, games_played_text, total_score_text)

        # Dibujar opciones ("Volver" y "Borrar datos")
        for index, option_text in enumerate(self.options):
            color = constants.YELLOW if self.selected_index == index else constants.WHITE
            option_surf = self.font.render(option_text, True, color)
            option_rect = option_surf.get_rect(center=(constants.WIDTH // 2, self.start_y + self.spacing_y * (5 + index)))
            self.screen.blit(option_surf, option_rect)

    # Metodo para dibujar las estadisticas
    def draw_stats(self, avg_score_text, best_score_text, games_played_text, total_score_text):
        # Renderizar las estadísticas
        best_score_surf = self.font.render(best_score_text, True, constants.WHITE)
        total_score_surf = self.font.render(total_score_text, True, constants.WHITE)
        avg_score_surf = self.font.render(avg_score_text, True, constants.WHITE)
        games_played_surf = self.font.render(games_played_text, True, constants.WHITE)

        # Mostrar cada estadística
        self.screen.blit(best_score_surf, (constants.WIDTH // 2 - best_score_surf.get_width() // 2, self.start_y))
        self.screen.blit(total_score_surf,
                         (constants.WIDTH // 2 - total_score_surf.get_width() // 2, self.start_y + self.spacing_y))
        self.screen.blit(avg_score_surf,
                         (constants.WIDTH // 2 - avg_score_surf.get_width() // 2, self.start_y + self.spacing_y * 2))
        self.screen.blit(games_played_surf,
                         (constants.WIDTH // 2 - games_played_surf.get_width() // 2, self.start_y + self.spacing_y * 3))

    # Metodo para cargar las estadisticas desde la clase utils
    def load_stats_from_utils(self):
        # Cargar estadísticas y mostrarlas en pantalla
        stats = load_stats()
        best_score_text = f"Mejor Puntaje: {stats['best_score']}"
        total_score_text = f"Total de Puntuación: {stats['total_score']:}"
        avg_score_text = f"Promedio de Puntuación: {stats['average_score']:.2f}"
        games_played_text = f"Partidas Jugadas: {stats['games_played']}"
        return avg_score_text, best_score_text, games_played_text, total_score_text

    # Metodo para dibujar el fondo animado
    def draw_animated_bg(self):
        # Dibujar fondo animado con desplazamiento (realmente es como duplicar el fondo uno seguido del otro)
        self.screen.blit(self.background_img, (constants.BACKGROUND_POSITION, 0))
        self.screen.blit(self.background_img, (constants.BACKGROUND_POSITION - self.bg_width, 0))
        # Actualizar la posición del fondo para que se desplace
        constants.BACKGROUND_POSITION += constants.BACKGROUND_SPEED  # Velocidad de desplazamiento
        # Si el fondo se ha desplazado completamente fuera de la pantalla, reiniciarlo
        if constants.BACKGROUND_POSITION >= self.bg_width:
            constants.BACKGROUND_POSITION = 0

    # Metodo para controlar las teclas
    def handle_keys(self, event):
        # Guardar el índice del último botón seleccionado
        last_index = self.selected_index

        # Navegar entre opciones con teclas de dirección
        if event.key in (pygame.K_DOWN, pygame.K_s):
            self.selected_index = (self.selected_index + 1) % len(self.options)
        elif event.key in (pygame.K_UP, pygame.K_w):
            self.selected_index = (self.selected_index - 1) % len(self.options)
        elif event.key == pygame.K_RETURN:
            return self.options[self.selected_index]  # Retorna la opción seleccionada
        elif event.key == pygame.K_ESCAPE:
            return "Volver"

        # Solo reproducir el sonido de hover si el índice ha cambiado
        if last_index != self.selected_index:
            self.hover_sound.set_volume(optionsMenu.global_sfx_volume / 100)
            self.hover_sound.play()

    # Metodo para controlar el ratón
    def handle_mouse(self, mouse_pos):
        # Guardar el índice del último botón seleccionado
        last_index = self.selected_index

        # Detectar si el mouse está sobre alguna opción
        for index, option_text in enumerate(self.options):
            # Calcular la posición de cada opción ("Volver" y "Borrar datos")
            option_y_position = self.start_y + self.spacing_y * (5 + index)

            # Crear un rectángulo para cada opción en la posición calculada
            option_rect = self.font.render(option_text, True, constants.WHITE).get_rect(
                center=(constants.WIDTH // 2, option_y_position))

            # Comprobar si el mouse está sobre el rectángulo de esta opción
            if option_rect.collidepoint(mouse_pos):
                self.selected_index = index  # Cambia el índice al botón correspondiente

        # Solo reproducir el sonido de hover si el índice ha cambiado
        if last_index != self.selected_index:
            self.hover_sound.set_volume(optionsMenu.global_sfx_volume / 100)
            self.hover_sound.play()

        return self.options[self.selected_index]  # Retorna la opción si el mouse está sobre ella

    # Metodo para reiniciar los datos del jugador
    def execute_option(self):
        # Ejecuta la opción seleccionada
        if self.options[self.selected_index] == "Borrar datos":
            reset_stats()  # Llama a la función para borrar datos
