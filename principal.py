# main.py
import sys

import pygame

import constants
import optionsMenu
from optionsMenu import OptionsMenu
from slime import Slime
from camera import Camera
from character import Character

from heart import Heart
from mainMenu import MainMenu
from projectile import Projectile
from statsMenu import StatsMenu
from utils import Utils
from utils import save_stats

# Inicializamos pygame
pygame.init()

# Obtener tamaño de pantalla del monitor
WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h

# Inicializar constantes con tamaño de pantalla
constants.initialize_constants(WIDTH, HEIGHT)

# Definir el tamaño inicial y el modo de la pantalla
screen = pygame.display.set_mode(constants.SIZE)  # Inicia en modo ventana
pygame.display.set_caption("Dodge & Charge")

# Variable para verificar si está en pantalla completa
fullscreen = False

# Variables de sonido
# Inicializar pygame mixer
pygame.mixer.init()

# Cargar sonidos
dodge_sound = pygame.mixer.Sound("sound/dodge_mode.wav")
charge_sound = pygame.mixer.Sound("sound/charge_mode.wav")
collision_sound = pygame.mixer.Sound("sound/collision_sound.ogg")
slime_death_sound = pygame.mixer.Sound("sound/slime_death.ogg")
fireball_sound = pygame.mixer.Sound("sound/fireball_sound.ogg")
# Ruta de las pistas
main_menu_sound = "sound/main_menu_soundtrack.wav"
fight_menu_sound = "sound/fight_soundtrack.wav"

# Instancia del Menú Opciones (se instancia primero para que carguen los ajustes antes)
options_menu = OptionsMenu(screen)
in_options_menu = False

# Variables de volumen de audio

music_volume = optionsMenu.global_music_volume # Volumen inicial de la música
sfx_volume = optionsMenu.global_sfx_volume    # Volumen inicial de efectos de sonido

# Aplicar volumen inicial
pygame.mixer.music.set_volume(music_volume/100)
dodge_sound.set_volume(sfx_volume/100)
charge_sound.set_volume(sfx_volume/100)
collision_sound.set_volume(sfx_volume/100)
slime_death_sound.set_volume(sfx_volume/100)
fireball_sound.set_volume(sfx_volume/350) # En 350 porque el sonido este está muy fuerte

# Variable para rastrear qué música está activa
current_music = None

# Título de la ventana
pygame.display.set_caption("Dodge & Charge")

# Cargar imagen de fondo
try:
    background_img = pygame.image.load(constants.BACKGROUND_IMG_PATH)
except pygame.error:
    print("No se pudo cargar la imagen de fondo.")
    pygame.quit()
    sys.exit()

# Configuración del personaje
player = Character(center_position=(WIDTH // 2, HEIGHT // 2), width=WIDTH, height=HEIGHT)

# Configuración de las slimes
slimes = []

# Evento personalizado
ADD_SLIME = pygame.USEREVENT + 1

# Configurar el temporizador para generar slimes
pygame.time.set_timer(ADD_SLIME, constants.SLIME_SPAWN_INTERVAL)

# Configuración de los proyectiles
projectiles = []
shooting = False
last_shot_time = 0

# Variables del sistema de modos
score = 0
clock = pygame.time.Clock()
mode = "DODGE"  # Estado inicial
mode_timer = 0  # Temporizador para cambiar de modo
mode_display_time = 2000  # Duración de la visualización de cambio de modo en ms
mode_change_time = 10000  # Tiempo para alternar modos (10 segundos)
show_mode_text = False  # Indica si mostrar el texto de modo

# Variables para el fondo dinámico
background_x = 0  # Posición inicial del fondo en X
background_speed = 1  # Velocidad de desplazamiento del fondo

# Instancia del Menú Principal
main_menu = MainMenu(screen)
in_main_menu = True  # Comienza en el menú principal

# Instancia del Menú Estadísticas
statistics_menu = StatsMenu(screen)
in_statistics_menu = False

# Verificación menú de juego
in_play_menu = False

# Cargar las imágenes para la animación de corazones
heart_images = Utils.load_animation(constants.CHARACTER_HEART_PATH, 8, constants.HEART_SIZE)

# Instancia de la animación de corazones con posición y vidas iniciales
heart_display = Heart(10, 50, heart_images, player.hearts)

# Inicializa el tamaño del nivel
LEVEL_WIDTH = 2000
LEVEL_HEIGHT = 2000

# Inicializa la cámara en el juego
camera = Camera(LEVEL_WIDTH, LEVEL_HEIGHT)

def increase_difficulty():
    global slimes

    # Reducir el intervalo de aparición de bolas
    if constants.SLIME_SPAWN_INTERVAL > 500:  # Limitar el intervalo mínimo a 500 ms
        constants.SLIME_SPAWN_INTERVAL -= 500
        pygame.time.set_timer(ADD_SLIME, constants.SLIME_SPAWN_INTERVAL)

    # Incrementar la velocidad de los slimes
    for slime in slimes:
        slime.speed[0] *= 1.05
        slime.speed[1] *= 1.05

# Temporizador para controlar la dificultad (cada 10 segundos)
difficulty_timer = pygame.time.get_ticks()

# Bucle principal del juego
run = True
while run:
    dt = clock.tick(60)

    btnSelected = None # Botón seleccionado del menú principal

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Evento para poder salir del juego
            run = False

        if in_main_menu: # Si se encuentra en el menú principal
            # Eventos del menú
            if event.type == pygame.MOUSEMOTION: # Controla los movimientos de la posición del ratón
                main_menu.handle_mouse(event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN: # Controla los clics del ratón
                btnSelected = main_menu.handle_mouse(event.pos)
            elif event.type == pygame.KEYDOWN: # Controla las teclas presionadas
                btnSelected = main_menu.handle_keys(event)
                if event.key == pygame.K_F11: # Si se le da a la tecla F11 se pone en Pantalla Completa
                    # Alternar entre pantalla completa y modo ventana
                    fullscreen = not fullscreen
                    if fullscreen:
                        screen = pygame.display.set_mode(
                            (pygame.display.Info().current_w, pygame.display.Info().current_h), pygame.FULLSCREEN) # Se ajusta a las dimensiones del monitor activo
                    else:
                        screen = pygame.display.set_mode(constants.SIZE)

            # Procesa acciones del menú principal
            if btnSelected == "Jugar":
                in_main_menu = False
                in_play_menu = True
            elif btnSelected == "Opciones":
                in_main_menu = False
                in_options_menu = True
            elif btnSelected == "Estadísticas":
                in_main_menu = False
                in_statistics_menu = True  # Cambiar al menú de estadísticas
            elif btnSelected == "Salir":
                run = False
        elif in_statistics_menu:
            if event.type == pygame.MOUSEMOTION:
                selected_option = statistics_menu.handle_mouse(event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                selected_option = statistics_menu.handle_mouse(event.pos)
                if selected_option == "Volver":
                    in_statistics_menu = False
                    in_main_menu = True
                elif selected_option == "Borrar datos":
                    statistics_menu.execute_option()  # Borra datos si esta opción está seleccionada
            elif event.type == pygame.KEYDOWN:
                selected_option = statistics_menu.handle_keys(event)
                if selected_option == "Volver":
                    in_statistics_menu = False
                    in_main_menu = True
                elif selected_option == "Borrar datos":
                    statistics_menu.execute_option()
        elif in_options_menu:
            # Manejar eventos para el menú de opciones
            if event.type == pygame.MOUSEMOTION:
                selected_option = options_menu.handle_mouse(event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                selected_option = options_menu.handle_mouse(event.pos)
                if selected_option == "Volver":
                    in_options_menu = False
                    in_main_menu = True

                    dodge_sound.set_volume(options_menu.sfx_volume / 100)
                    charge_sound.set_volume(options_menu.sfx_volume / 100)
                    collision_sound.set_volume(options_menu.sfx_volume / 100)
                    slime_death_sound.set_volume(options_menu.sfx_volume / 100)
                    fireball_sound.set_volume(options_menu.sfx_volume / 350)
            elif event.type == pygame.KEYDOWN:
                selected_option = options_menu.handle_keys(event)

                if selected_option == "Volver":
                    in_options_menu = False
                    in_main_menu = True

                    dodge_sound.set_volume(options_menu.sfx_volume / 100)
                    charge_sound.set_volume(options_menu.sfx_volume / 100)
                    collision_sound.set_volume(options_menu.sfx_volume / 100)
                    slime_death_sound.set_volume(options_menu.sfx_volume / 100)
                    fireball_sound.set_volume(options_menu.sfx_volume / 350)




        elif in_play_menu:
            if event.type == ADD_SLIME:
                slimes.append(Slime(player.rect))  # Creación de slimes aleatorias (con distancia de seguridad frente al jugador)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if mode == "CHARGE" and event.button == 1:  # Botón izquierdo del ratón

                    shooting = True  # Activar estado de disparo
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    shooting = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False  # Salir del juego con la tecla ESC
                elif event.key == pygame.K_F11:
                    # Alternar entre pantalla completa y modo ventana
                    fullscreen = not fullscreen
                    if fullscreen:
                        screen = pygame.display.set_mode(
                            (pygame.display.Info().current_w, pygame.display.Info().current_h), pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode(constants.SIZE)

        # Si está en el menú, dibujarlo; si no, correr el juego
    if in_main_menu:
        # Si la música actual no es la del menú principal, cambiarla
        if current_music != "main_menu":
            pygame.mixer.music.fadeout(500)  # Transición suave
            pygame.mixer.music.load(main_menu_sound)
            pygame.mixer.music.play(-1)  # Reproducir en bucle
            current_music = "main_menu"  # Actualizar el estado de música actual
        main_menu.draw()
    elif in_statistics_menu:
        statistics_menu.draw()
    elif in_options_menu:

        options_menu.draw()
    elif in_play_menu:
        # Si la música actual no es la del menú de juego, cambiarla
        if current_music != "fight_menu":
            pygame.mixer.music.fadeout(500)  # Transición suave
            pygame.mixer.music.load(fight_menu_sound)
            pygame.mixer.music.play(-1)  # Reproducir en bucle
            current_music = "fight_menu"  # Actualizar el estado de música actual

        keys = pygame.key.get_pressed()

        # Movimiento del personaje
        player.move(keys)

        # Actualizar la posición de la cámara según la posición del personaje
        camera.update(player)

        # Manejar el disparo de proyectiles
        if shooting:
            current_time = pygame.time.get_ticks()
            if current_time - last_shot_time >= constants.SHOOT_INTERVAL:
                last_shot_time = current_time
                mouse_pos = pygame.Vector2(pygame.mouse.get_pos())  # Posición del ratón
                player_pos = pygame.Vector2(player.rect.center)  # Posición del jugador
                center_pos = WIDTH / 2, HEIGHT / 2

                # Dirección calculada desde la posición del centro hacia la posición del ratón (se podría mejorar)
                dir = (mouse_pos - center_pos).normalize()

                # Crear el proyectil
                projectiles.append(Projectile(start_pos=player_pos, dir=dir))
                fireball_sound.play()

        # Dibujar fondo y personaje
        screen.blit(background_img, camera.apply(background_img.get_rect()))
        player.draw(screen, camera)

        # Mover proyectiles y verificar colisiones
        for projectile in projectiles[:]:
            projectile.move()

            # Verificar colisiones con los slimes
            for slime in slimes[:]:
                if projectile.rect.colliderect(slime.rect):
                    score += 5  # Incrementamos el puntaje
                    slime_death_sound.play()
                    slimes.remove(slime)
                    projectiles.remove(projectile)
                    break

            # Eliminar proyectiles fuera de la pantalla
            if projectile.is_off_screen():
                projectiles.remove(projectile)

        # Mover y verificar colisiones de los slimes
        for slime in slimes[:]:
            slime.move(player.rect, mode)
            if player.rect.colliderect(slime.rect):
                collision_sound.play()
                player.hearts -= 1
                heart_display.lives -= 1
                slimes.remove(slime)
                camera.start_shake(duration=15, intensity=10)  # Efecto de temblor

                if player.hearts == 0 and not player.is_dead:
                    player.is_dead = True  # Activar estado de muerte
                    player.set_direction("death")
                    player.animation_index = 0 # Reiniciar la animación de muerte
                    player.animation_counter = 0

                if player.is_dead:
                    if player.animate(False):  # Si la animación de muerte terminó
                        # save_stats(score)  # Guardar estadísticas antes de salir
                        # Podrías reiniciar el juego en lugar de cerrar
                        # in_play_menu = False
                        # in_main_menu = True
                        # Resetear estados relevantes:
                        # slimes = []
                        # projectiles = []
                        # player.hearts = 3
                        # heart_display.lives = 3
                        # player.is_dead = False
                        pass

        # Dibujar slimes ajustados con la cámara
        for slime in slimes:
            # Obtener el frame actual de la animación
            frame = slime.animations[slime.animation_index]

            # Verificar si el slime está volteada horizontalmente
            if slime.flipped:
                frame = pygame.transform.flip(frame, True, False)  # Voltear horizontalmente si está flipped

            # Dibujar el slime ajustado con la cámara
            screen.blit(frame, camera.apply(slime.rect))


        # Actualizar la animación de los corazones
        heart_display.update()

        # Dibujar los corazones en pantalla
        heart_display.draw(screen)

        # Dibujar proyectiles ajustados con la cámara
        for projectile in projectiles:
            screen.blit(projectile.image, camera.apply(projectile.rect))


        mode_timer += dt  # Incrementa el temporizador del modo actual
        # Alterna el modo cada 10 segundos
        if mode_timer >= mode_change_time:
            mode = "CHARGE" if mode == "DODGE" else "DODGE"
            if mode == "DODGE":
                dodge_sound.play()
            else:
                charge_sound.play()
            mode_timer = 0
            show_mode_text = True  # Activa la visualización del texto de cambio de modo
            mode_display_timer = pygame.time.get_ticks()  # Inicia el temporizador para el texto
            shooting = False

        # Muestra texto de modo en pantalla durante 2 segundos
        if show_mode_text:
            # Cargar la fuente personalizada para el texto del modo
            font_big = pygame.font.Font(constants.FONT_PATH, constants.MODE_FONT_SIZE)

            # Renderizar el texto del modo
            mode_text = font_big.render(mode, True, constants.WHITE)

            # Posición para centrar el texto
            text_x = constants.WIDTH // 2 - mode_text.get_width() // 2
            text_y = constants.HEIGHT // 4

            # Dibujar el texto en la pantalla
            screen.blit(mode_text, (text_x, text_y))

            # Verifica si se ha cumplido el tiempo para ocultar el texto
            if pygame.time.get_ticks() - mode_display_timer >= mode_display_time:
                show_mode_text = False

            # Incrementar la dificultad cada 10 segundos
            if pygame.time.get_ticks() - difficulty_timer > 10000:  # Cada 10 segundos
                increase_difficulty()
                difficulty_timer = pygame.time.get_ticks()

        # Mostrar puntaje en la pantalla
        font = pygame.font.Font(constants.FONT_PATH, constants.FONT_SIZE)
        score_text = font.render(f"Puntos: {score}", True,
                                     constants.WHITE)
        screen.blit(score_text, (10, 10))

    pygame.display.flip()

pygame.quit()
