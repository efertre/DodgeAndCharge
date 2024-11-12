import pygame
import json
import os
from datetime import datetime

STATS_FILE = "stats.json"

class Utils:
    @staticmethod
    def load_animation(path, num_images, scale):
        """Carga y escala una serie de imágenes para la animación."""
        images = []
        for i in range(1, num_images + 1):
            img = pygame.image.load(f"{path}{i}.png")
            images.append(pygame.transform.scale(img, scale))
        return images

# Función para inicializar las estadísticas si el archivo no existe
def initialize_statistics():
    return {
        "best_score": 0,
        "total_score": 0,
        "games_played": 0,
        "average_score": 0.0
    }

# Función para guardar estadísticas después de cada partida
def save_stats(score):
    # Cargar estadísticas existentes o inicializarlas si el archivo no existe
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, "r") as file:
            stats = json.load(file)
    else:
        stats = initialize_statistics()

    # Actualizar el mejor puntaje si el puntaje actual es mayor
    if score > stats["best_score"]:
        stats["best_score"] = score

    # Sumar el puntaje actual al total acumulado y aumentar el contador de partidas
    stats["total_score"] += score
    stats["games_played"] += 1

    # Calcular la media de puntuación
    stats["average_score"] = stats["total_score"] / stats["games_played"]

    # Guardar estadísticas actualizadas en el archivo
    with open(STATS_FILE, "w") as file:
        json.dump(stats, file, indent=4)

# Función para cargar estadísticas
def load_stats():
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, "r") as file:
            return json.load(file)
    return initialize_statistics()

def reset_stats():
    # Verifica si el archivo existe y lo resetea con valores iniciales
    if os.path.exists(STATS_FILE):
        # Datos iniciales para las estadísticas
        default_stats = {
            "best_score": 0,
            "total_score": 0,
            "average_score": 0.0,
            "games_played": 0
        }
        # Abre el archivo en modo escritura ("w") y escribe los datos predeterminados
        with open(STATS_FILE, "w") as file:
            json.dump(default_stats, file, indent=4)  # Guarda como JSON formateado


