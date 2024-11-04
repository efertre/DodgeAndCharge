import sys
import pygame
import random
import constants
import math

# Inicializamos pygame
pygame.init()

# Configuración de pantalla
screen = pygame.display.set_mode(constants.SIZE)
pygame.display.set_caption("Dodge & Charge")

# Cargar imagen de fondo
try:
    background_img = pygame.image.load(constants.BACKGROUND_IMG_PATH)
except pygame.error:
    print("No se pudo cargar la imagen de fondo.")
    pygame.quit()
    sys.exit()

# Función para cargar y escalar imágenes de animación
def load_animation_images(path, num_images, size):
    """Carga y escala una serie de imágenes para la animación."""
    images = []
    for i in range(1, num_images + 1):
        img = pygame.image.load(f"{path}{i}.png")
        scaled_img = pygame.transform.scale(img, size)  # Escalar imagen
        images.append(scaled_img)
    return images

# Cargar y escalar las animaciones para cada dirección del personaje
character_up = load_animation_images(constants.CHARACTER_UP_PATH, 1, constants.CHARACTER_SIZE)
character_down = load_animation_images(constants.CHARACTER_DOWN_PATH, 1, constants.CHARACTER_SIZE)
character_left = load_animation_images(constants.CHARACTER_LEFT_PATH, 3, constants.CHARACTER_SIZE)
character_right = load_animation_images(constants.CHARACTER_RIGHT_PATH, 3, constants.CHARACTER_SIZE)

# Cargar y escalar la imagen de la bola
try:
    ball_img = pygame.image.load(constants.BALL_IMG_PATH)
    ball_img = pygame.transform.scale(ball_img, constants.BALL_SIZE)  # Escalar la bola
except pygame.error:
    print("No se pudo cargar la imagen de la pelota.")
    pygame.quit()
    sys.exit()

# Cargar y escalar la imagen del proyectil
try:
    projectile_img = pygame.image.load(constants.PROJECTILE_IMG_PATH)  # Ruta a la imagen del proyectil
    projectile_img = pygame.transform.scale(projectile_img, (10, 10))  # Tamaño del proyectil
except pygame.error:
    print("No se pudo cargar la imagen del proyectil.")
    pygame.quit()
    sys.exit()

# Configuración de animación y personaje
characterrect = character_down[0].get_rect()
characterrect.center = (constants.WIDTH // 2, constants.HEIGHT // 2)
current_direction = character_down
animation_index = 0
animation_counter = 0

# Configuración de las bolas
balls = []
ADD_BALL = pygame.USEREVENT + 1
pygame.time.set_timer(ADD_BALL, constants.BALL_SPAWN_INTERVAL)


# Variables del sistema de modos
score = 0
clock = pygame.time.Clock()
mode = "DODGE"  # Estado inicial
mode_timer = 0  # Temporizador para cambiar de modo
mode_display_time = 2000  # Duración de la visualización de cambio de modo en ms
mode_change_time = 10000  # Tiempo para alternar modos (10 segundos)
show_mode_text = False  # Indica si mostrar el texto de modo

# Lista para proyectiles
projectiles = []
shooting = False  # Bandera para saber si el botón está presionado
# Inicializar el temporizador de disparo
last_shot_time = 0


# Bucle principal del juego
run = True
while run:
    # Manejamos el tiempo transcurrido
    dt = clock.tick(60)  # Limitamos a 60 FPS
    score += 1  # Incrementamos el puntaje en cada ciclo
    mode_timer += dt  # Incrementa el temporizador del modo actual
    mouse_x, mouse_y = pygame.mouse.get_pos()  # Obtener la posición del ratón


    # Alterna el modo cada 10 segundos
    if mode_timer >= mode_change_time:
        mode = "CHARGE" if mode == "DODGE" else "DODGE"
        mode_timer = 0
        show_mode_text = True  # Activa la visualización del texto de cambio de modo
        mode_display_timer = pygame.time.get_ticks()  # Inicia el temporizador para el texto
        shooting = False

    # Captura de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == ADD_BALL:
            # Añadir una bola en una posición aleatoria con velocidad aleatoria
            ballrect = ball_img.get_rect()
            ballrect.topleft = (random.randint(0, constants.WIDTH - ballrect.width),
                                random.randint(0, constants.HEIGHT - ballrect.height))
            balls.append({
                "rect": ballrect,
                "speed": [random.choice([-1, 1]) * random.randint(*constants.BALL_SPEED_RANGE),
                          random.choice([-1, 1]) * random.randint(*constants.BALL_SPEED_RANGE)]
            })
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if mode == "CHARGE" and event.button == 1:  # Botón izquierdo del ratón
                print("Pulsa")
                shooting = True  # Activar estado de disparo

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Cuando el botón izquierdo se suelta
                print("Deja de pulsar")
                shooting = False  # Desactivar estado de disparo

    # Generación de proyectiles mientras el botón esté presionado y en intervalos controlados
    if shooting:
        current_time = pygame.time.get_ticks()  # Obtener el tiempo actual
        if current_time - last_shot_time >= constants.SHOOT_INTERVAL:
            last_shot_time = current_time  # Reiniciar el temporizador de disparo

            # Obtener la posición del ratón
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Calcular la dirección del proyectil hacia el ratón
            dx, dy = mouse_x - characterrect.centerx, mouse_y - characterrect.centery
            distance = math.hypot(dx, dy)
            if distance != 0:
                dx, dy = dx / distance, dy / distance  # Normalizar la dirección

            # Crear el proyectil y añadirlo a la lista
            projectile_rect = projectile_img.get_rect(center=characterrect.center)
            projectiles.append({
                "rect": projectile_rect,
                "direction": (dx, dy)
            })

    # Mover los proyectiles
    # Mover proyectiles
    for projectile in projectiles[:]:
        dx, dy = projectile["direction"]
        projectile["rect"].move_ip(dx * constants.PROJECTILE_SPEED, dy * constants.PROJECTILE_SPEED)

        # Verificar si colisionan con bolas
        for ball in balls[:]:
            if projectile["rect"].colliderect(ball["rect"]):
                balls.remove(ball)  # Elimina la bola
                projectiles.remove(projectile)  # Elimina el proyectil
                break

        # Eliminar proyectiles que salen de la pantalla
        if (projectile["rect"].bottom < 0 or projectile["rect"].top > constants.HEIGHT or
                projectile["rect"].left < 0 or projectile["rect"].right > constants.WIDTH):
            projectiles.remove(projectile)

    # Movimiento del personaje y cambio de dirección
    keys = pygame.key.get_pressed()

    moving = False
    new_direction = current_direction

    if (keys[pygame.K_UP] or keys[pygame.K_w]) and characterrect.top > 0:
        characterrect.move_ip(0, -constants.CHARACTER_SPEED)
        new_direction = character_up
        moving = True
    elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and characterrect.bottom < constants.HEIGHT:
        characterrect.move_ip(0, constants.CHARACTER_SPEED)
        new_direction = character_down
        moving = True
    elif (keys[pygame.K_LEFT] or keys[pygame.K_a]) and characterrect.left > 0:
        characterrect.move_ip(-constants.CHARACTER_SPEED, 0)
        new_direction = character_left
        moving = True
    elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and characterrect.right < constants.WIDTH:
        characterrect.move_ip(constants.CHARACTER_SPEED, 0)
        new_direction = character_right
        moving = True

    if new_direction != current_direction:
        current_direction = new_direction
        animation_index = 0

    if moving:
        animation_counter += constants.ANIMATION_SPEED
        if animation_counter >= 1:
            animation_index = (animation_index + 1) % len(current_direction)
            animation_counter = 0
    else:
        animation_index = 0

    # Mover y rebotar bolas
    for ball in balls:
        speed_factor =  1
        ball["rect"] = ball["rect"].move([s * speed_factor for s in ball["speed"]])

        if ball["rect"].left < 0 or ball["rect"].right > constants.WIDTH:
            ball["speed"][0] = -ball["speed"][0]
        if ball["rect"].top < 0 or ball["rect"].bottom > constants.HEIGHT:
            ball["speed"][1] = -ball["speed"][1]

        if characterrect.colliderect(ball["rect"]):
            run = False

    # Dibujar pantalla
    screen.blit(background_img, (0, 0))
    screen.blit(current_direction[animation_index], characterrect)

    for ball in balls:
        screen.blit(ball_img, ball["rect"])

    # Dibujar proyectiles
    for projectile in projectiles:
        screen.blit(projectile_img, projectile["rect"])

    # Muestra texto de modo en pantalla durante 2 segundos
    if show_mode_text:
        font_big = pygame.font.Font(None, 80)
        mode_text = font_big.render(mode, True, constants.RED)
        screen.blit(mode_text, (constants.WIDTH // 2 - mode_text.get_width() // 2, constants.HEIGHT // 4))

        # Verifica si se ha cumplido el tiempo para ocultar el texto
        if pygame.time.get_ticks() - mode_display_timer >= mode_display_time:
            show_mode_text = False

    # Actualizar la pantalla
    pygame.display.flip()

pygame.quit()
