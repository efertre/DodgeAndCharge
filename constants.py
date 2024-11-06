# Constantes y configuraciones

# Configuración de pantalla
WIDTH = 800
HEIGHT = 600
SIZE = (WIDTH, HEIGHT)

# Colores
WHITE = (255, 255, 255)
GRAY =  (128,128,128)
BLACK = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 255, 255)

# Velocidades
CHARACTER_SPEED = 5
BALL_SPEED_RANGE = [2, 5]
ANIMATION_SPEED = 0.1  # Cambia de fotograma cada cierto tiempo
PROJECTILE_SPEED = 8  # Velocidad de dipsaro (en milisegundos)
SHOOT_INTERVAL = 750  # Frecuencia de disparo (en milisegundos)


# Rutas de imágenes
BACKGROUND_IMG_PATH = "background/background.png"
MAIN_MENU_BACKGROUND_IMG_PATH = "background/main_menu_background.png"
CHARACTER_UP_PATH = "assets/character/up/up_"
CHARACTER_DOWN_PATH = "assets/character/down/down_"
CHARACTER_LEFT_PATH = "assets/character/left/left_"
CHARACTER_RIGHT_PATH = "assets/character/right/right_"
CHARACTER_HEART_PATH = "assets/character/heart/heart_"
BALL_IMG_PATH = "assets/ball/ball.png"
PROJECTILE_IMG_PATH = "assets/projectile/projectile.png"

# Tamaño del personaje y las bolas
CHARACTER_SIZE = (50, 60)  # Ancho y alto del personaje
BALL_SIZE = (30, 30)       # Ancho y alto de la bola
PROJECTILE_SIZE = (20,20) # Ancho y alto deL proyectil
HEART_SIZE = (25,25) # Ancho y alto del corazón

# Configuración de bolas
BALL_SPAWN_INTERVAL = 5000  # en milisegundos (5 segundos)
POWER_SPAWN_INTERVAL = 15000 # AÚN QUEDA POR IMPLEMENTAR
POWER_DURATION = 10000 # AÚN QUEDA POR IMPLEMENTAR

# Fuente
TITLE_FONT_SIZE = 60
SUBTITLE_FONT_SIZE = 25
BUTTON_FONT_SIZE = 20
FONT_SIZE = 18
MODE_FONT_SIZE = 80 # Tamaño para la fuente de cambiar de modo
FONT_PATH = "assets/fonts/pixel.ttf" # Fuente pixelada personalizada
