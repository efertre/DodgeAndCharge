# Inicializar dimensiones predeterminadas
WIDTH = 800  # Un valor predeterminado
HEIGHT = 600  # Un valor predeterminado
SIZE = (WIDTH, HEIGHT)

# Colores
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# Velocidades
CHARACTER_SPEED = 5
BALL_SPEED_RANGE = [2, 5]
ANIMATION_SPEED = 0.1
PROJECTILE_SPEED = 10
SHOOT_INTERVAL = 500

# Rutas de imágenes
BACKGROUND_IMG_PATH = "assets/background/background.png"
MAIN_MENU_BACKGROUND_IMG_PATH = "assets/background/main_menu_background.png"
STATS_MENU_BACKGROUND_IMG_PATH = "assets/background/main_menu_background_blurred.png"
CHARACTER_UP_PATH = "assets/character/up/up_"
CHARACTER_DOWN_PATH = "assets/character/down/down_"
CHARACTER_LEFT_PATH = "assets/character/left/left_"
CHARACTER_RIGHT_PATH = "assets/character/right/right_"
CHARACTER_HEART_PATH = "assets/character/heart/heart_"
SLIME_IMG_PATH = "assets/green_slime/green_slime_0"
PROJECTILE_IMG_PATH = "assets/projectile/projectile.png"

# Posición del fondo animado del menú stats y principal
BACKGROUND_POSITION = 0
BACKGROUND_SPEED = 1

# Tamaños (se inicializan en initialize_constants)
CHARACTER_SIZE = None
SLIME_SIZE = None
SLIME_SIZE = None
PROJECTILE_SIZE = None
HEART_SIZE = None
TITLE_FONT_SIZE = None
SUBTITLE_FONT_SIZE = None
BUTTON_FONT_SIZE = None
FONT_SIZE = None
MODE_FONT_SIZE = None

# Límites del mapa
MOVEMENT_MARGIN_TOP = 350
MOVEMENT_MARGIN_BOTTOM = 950
MOVEMENT_MARGIN_LEFT = 270
MOVEMENT_MARGIN_RIGHT = 250
# Fuente
FONT_PATH = "assets/fonts/pixel.ttf"

# Configuración de bolas
BALL_SPAWN_INTERVAL = 2500  # en milisegundos (2.5 segundos)
POWER_SPAWN_INTERVAL = 15000  # AÚN QUEDA POR IMPLEMENTAR
POWER_DURATION = 10000  # AÚN QUEDA POR IMPLEMENTAR


# Función para inicializar el tamaño de pantalla
def initialize_constants(width, height):
    global WIDTH, HEIGHT, SIZE, SCALE, CHARACTER_SIZE, SLIME_SIZE, PROJECTILE_SIZE, HEART_SIZE
    global TITLE_FONT_SIZE, SUBTITLE_FONT_SIZE, BUTTON_FONT_SIZE, FONT_SIZE, MODE_FONT_SIZE

    WIDTH = width
    HEIGHT = height
    SIZE = (WIDTH, HEIGHT)

    # Factor de escala basado en la resolución
    SCALE = WIDTH / 1920  # Basado en una referencia de 1920x1080

    # Escalar tamaños usando SCALE
    CHARACTER_SIZE = (int(70 * SCALE), int(80 * SCALE))
    SLIME_SIZE = (int(100 * SCALE), int(100 * SCALE))
    PROJECTILE_SIZE = (int(30 * SCALE), int(30 * SCALE))
    HEART_SIZE = (int(50 * SCALE), int(50 * SCALE))  # Escalado

    # Escalar fuentes
    TITLE_FONT_SIZE = int(60 * SCALE)
    SUBTITLE_FONT_SIZE = int(25 * SCALE)
    BUTTON_FONT_SIZE = int(20 * SCALE)
    FONT_SIZE = int(28 * SCALE)
    MODE_FONT_SIZE = int(80 * SCALE)
