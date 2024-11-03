import sys
import pygame
import random
import constants

# Inicializamos pygame
pygame.init()

# Configuración de pantalla
screen = pygame.display.set_mode(constants.SIZE)
pygame.display.set_caption("Dodge & Charge")

# Cargar y escalar imagen de fondo
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

# Configuración de poderes
powers = []
ADD_POWER = pygame.USEREVENT + 2
pygame.time.set_timer(ADD_POWER, constants.POWER_SPAWN_INTERVAL)

# Variables de poderes
invulnerable = False
speed_boost = False
slow_balls = False
power_timer = 0

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
PROJECTILE_SPEED = 5

# Bucle principal del juego
run = True
while run:
    # Manejamos el tiempo transcurrido
    dt = clock.tick(60)  # Limitamos a 60 FPS
    score += 1  # Incrementamos el puntaje en cada ciclo
    mode_timer += dt  # Incrementa el temporizador del modo actual

    # Alterna el modo cada 10 segundos
    if mode_timer >= mode_change_time:
        mode = "CHARGE" if mode == "DODGE" else "DODGE"
        mode_timer = 0
        show_mode_text = True  # Activa la visualización del texto de cambio de modo
        mode_display_timer = pygame.time.get_ticks()  # Inicia el temporizador para el texto

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
        elif event.type == ADD_POWER:
            # Añadir un poder en una posición aleatoria
            powerrect = pygame.Rect(random.randint(0, constants.WIDTH - 20),
                                    random.randint(0, constants.HEIGHT - 20), 20, 20)
            powers.append({
                "rect": powerrect,
                "type": random.choice(["invulnerable", "speed_boost", "slow_balls"])
            })

    # Movimiento del personaje y cambio de dirección
    keys = pygame.key.get_pressed()
    moving = False
    new_direction = current_direction

    if keys[pygame.K_UP] and characterrect.top > 0:
        characterrect.move_ip(0, -constants.CHARACTER_SPEED * (2 if speed_boost else 1))
        new_direction = character_up
        moving = True
    elif keys[pygame.K_DOWN] and characterrect.bottom < constants.HEIGHT:
        characterrect.move_ip(0, constants.CHARACTER_SPEED * (2 if speed_boost else 1))
        new_direction = character_down
        moving = True
    elif keys[pygame.K_LEFT] and characterrect.left > 0:
        characterrect.move_ip(-constants.CHARACTER_SPEED * (2 if speed_boost else 1), 0)
        new_direction = character_left
        moving = True
    elif keys[pygame.K_RIGHT] and characterrect.right < constants.WIDTH:
        characterrect.move_ip(constants.CHARACTER_SPEED * (2 if speed_boost else 1), 0)
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

    # Disparar proyectiles en modo "CHARGE"
    if mode == "CHARGE" and keys[pygame.K_SPACE]:  # Cambia la tecla según lo que desees
        projectile_rect = projectile_img.get_rect(center=characterrect.center)
        projectiles.append({"rect": projectile_rect, "direction": current_direction})

    # Mover los proyectiles
    for projectile in projectiles[:]:  # Iterar sobre una copia de la lista
        if projectile["direction"] == character_up:
            projectile["rect"].move_ip(0, -PROJECTILE_SPEED)
        elif projectile["direction"] == character_down:
            projectile["rect"].move_ip(0, PROJECTILE_SPEED)
        elif projectile["direction"] == character_left:
            projectile["rect"].move_ip(-PROJECTILE_SPEED, 0)
        elif projectile["direction"] == character_right:
            projectile["rect"].move_ip(PROJECTILE_SPEED, 0)

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

    # Mover y rebotar bolas
    for ball in balls:
        speed_factor = 0.5 if slow_balls else 1
        ball["rect"] = ball["rect"].move([s * speed_factor for s in ball["speed"]])

        if ball["rect"].left < 0 or ball["rect"].right > constants.WIDTH:
            ball["speed"][0] = -ball["speed"][0]
        if ball["rect"].top < 0 or ball["rect"].bottom > constants.HEIGHT:
            ball["speed"][1] = -ball["speed"][1]

        if characterrect.colliderect(ball["rect"]) and not invulnerable:
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
