# Constantes y configuraciones

# Configuración de pantalla
WIDTH = 800
HEIGHT = 600
SIZE = (WIDTH, HEIGHT)

# Colores
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Velocidades
CHARACTER_SPEED = 5
BALL_SPEED_RANGE = [2, 5]
ANIMATION_SPEED = 0.1  # Cambia de fotograma cada cierto tiempo
PROJECTILE_SPEED = 10

# Configuración de la frecuencia de disparo (en milisegundos)
SHOOT_INTERVAL = 5  # Tiempo entre disparos en milisegundos
# Rutas de imágenes
BACKGROUND_IMG_PATH = "background/background.png"
CHARACTER_UP_PATH = "character/up_"
CHARACTER_DOWN_PATH = "character/down_"
CHARACTER_LEFT_PATH = "character/left_"
CHARACTER_RIGHT_PATH = "character/right_"
BALL_IMG_PATH = "ball.png"
PROJECTILE_IMG_PATH = "proyectil.png"

# Tamaño del personaje y las bolas
CHARACTER_SIZE = (30, 40)  # Ancho y alto del personaje
BALL_SIZE = (30, 30)       # Ancho y alto de la bola

# Configuración de bolas
BALL_SPAWN_INTERVAL = 5000  # en milisegundos (5 segundos)
POWER_SPAWN_INTERVAL = 15000
POWER_DURATION = 10000
# Fuente
FONT_SIZE = 36