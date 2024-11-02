import sys
import pygame
import random

import constants

# Inicializamos pygame
pygame.init()

# Configuración de pantalla y colores
screen = pygame.display.set_mode(constants.SIZE)
pygame.display.set_caption("One Game")

# Cargar imagen de fondo
try:
    background_img = pygame.image.load(constants.BACKGROUND_IMG_PATH)
except pygame.error:
    print("No se pudo cargar la imagen de fondo.")
    pygame.quit()
    sys.exit()


# Cargar animaciones de movimiento
def load_animation_images(path, num_images):
    """Carga una serie de imágenes para la animación."""
    images = []
    for i in range(1, num_images + 1):
        img = pygame.image.load(f"{path}{i}.png")
        images.append(img)
    return images


# Cargar las animaciones para cada dirección
character_up = load_animation_images(constants.CHARACTER_UP_PATH, 1)
character_down = load_animation_images(constants.CHARACTER_DOWN_PATH, 1)
character_left = load_animation_images(constants.CHARACTER_LEFT_PATH, 3)
character_right = load_animation_images(constants.CHARACTER_RIGHT_PATH, 3)

# Verificar la carga de imágenes para cada dirección
print("Frames en character_up:", len(character_up))
print("Frames en character_down:", len(character_down))
print("Frames en character_left:", len(character_left))
print("Frames en character_right:", len(character_right))

# Configurar las bolas
try:
    ball_img = pygame.image.load(constants.BALL_IMG_PATH)
except pygame.error:
    print("No se pudo cargar la imagen de la pelota.")
    pygame.quit()
    sys.exit()

# Inicializar el rectángulo del personaje
characterrect = character_down[0].get_rect()
characterrect.center = (constants.WIDTH // 2, constants.HEIGHT // 2)

# Configuración de animación
current_direction = character_down
animation_index = 0
animation_counter = 0

# Configuración de las bolas
balls = []
ADD_BALL = pygame.USEREVENT + 1
pygame.time.set_timer(ADD_BALL, constants.BALL_SPAWN_INTERVAL)

# Sistema de puntos
score = 0
clock = pygame.time.Clock()

# Bucle principal del juego
run = True
while run:
    # Manejamos el tiempo transcurrido
    clock.tick(60)  # Limitamos a 60 FPS
    score += 1  # Incrementamos el puntaje en cada ciclo

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

    # Movimiento del personaje y cambio de dirección
    keys = pygame.key.get_pressed()
    moving = False
    new_direction = current_direction  # Variable para detectar cambio de dirección

    if keys[pygame.K_UP] and characterrect.top > 0:
        characterrect.move_ip(0, -constants.CHARACTER_SPEED)
        new_direction = character_up
        moving = True
    elif keys[pygame.K_DOWN] and characterrect.bottom < constants.HEIGHT:
        characterrect.move_ip(0, constants.CHARACTER_SPEED)
        new_direction = character_down
        moving = True
    elif keys[pygame.K_LEFT] and characterrect.left > 0:
        characterrect.move_ip(-constants.CHARACTER_SPEED, 0)
        new_direction = character_left
        moving = True
    elif keys[pygame.K_RIGHT] and characterrect.right < constants.WIDTH:
        characterrect.move_ip(constants.CHARACTER_SPEED, 0)
        new_direction = character_right
        moving = True

    # Reinicia el índice de animación si hay un cambio de dirección
    if new_direction != current_direction:
        current_direction = new_direction
        animation_index = 0  # Reinicia el índice al cambiar de dirección

    # Actualizar la animación si el personaje se está moviendo
    if moving:
        animation_counter += constants.ANIMATION_SPEED
        if animation_counter >= 1:
            animation_index = (animation_index + 1) % len(current_direction)
            animation_counter = 0
    else:
        animation_index = 0  # Reinicia la animación si no se está moviendo

    # Mover y rebotar cada bola
    for ball in balls:
        ball["rect"] = ball["rect"].move(ball["speed"])
        # Rebote en los bordes de la pantalla
        if ball["rect"].left < 0 or ball["rect"].right > constants.WIDTH:
            ball["speed"][0] = -ball["speed"][0]
        if ball["rect"].top < 0 or ball["rect"].bottom > constants.HEIGHT:
            ball["speed"][1] = -ball["speed"][1]
        # Detectar colisión con el personaje
        if characterrect.colliderect(ball["rect"]):
            run = False  # Termina el juego si hay colisión

    # Dibujar la pantalla
    screen.blit(background_img, (0, 0))  # Dibuja el fondo en la esquina superior izquierda
    screen.blit(current_direction[animation_index], characterrect)  # Dibuja el fotograma actual de la animación
    for ball in balls:
        screen.blit(ball_img, ball["rect"])

    # Mostrar puntaje en la pantalla
    font = pygame.font.Font(None, constants.FONT_SIZE)
    score_text = font.render(f"Puntos: {score // 60}", True, constants.BLACK)  # Dividimos para obtener puntos por segundo
    screen.blit(score_text, (10, 10))

    # Actualizar la pantalla
    pygame.display.flip()

# Termina pygame
pygame.quit()
