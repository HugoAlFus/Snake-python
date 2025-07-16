"""
Autor: Hugo Almodóvar Fuster
Versión: 1.0
Descripción:
Clase que representa la comida en el juego de la serpiente.
Puede mostrarse como una imagen (manzana) o como un círculo básico si no se carga el sprite.
Incluye lógica para detectar si la serpiente ha "comido" la comida.
"""

import math
import os
import random
import cv2

from snake_game.util.overlay import overlay_image  # Utilidad para superponer imágenes con transparencia


class Food:
    def __init__(self, frame_width, frame_height):
        """
        Inicializa una nueva instancia de comida.

        Parámetros:
        - frame_width: Ancho del frame del juego.
        - frame_height: Alto del frame del juego.
        """
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.radius = 15  # Radio del área de colisión/comida
        self.position = self._generate_random_position()

        # Cargar sprite de manzana desde carpeta de assets
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "sprites", "food"))
        apple_path = os.path.join(base_path, "apple.png")

        self.image = cv2.imread(apple_path, cv2.IMREAD_UNCHANGED)  # Leer con canal alfa (RGBA)
        if self.image is not None:
            self.image = cv2.resize(self.image, (30, 30))

    def _generate_random_position(self):
        """
        Genera una posición aleatoria dentro de los límites del frame, evitando los bordes.
        """
        margin = 50
        x = random.randint(margin, self.frame_width - margin)
        y = random.randint(margin, self.frame_height - margin)
        return x, y

    def draw(self, frame):
        """
        Dibuja la comida en el frame. Usa imagen si está cargada, si no, un círculo de fallback.

        Parámetros:
        - frame: Imagen del juego (frame de cámara) sobre el que se dibuja.
        """
        if self.image is not None:
            x, y = self.position
            h, w = self.image.shape[:2]
            overlay_image(frame, self.image, x - w // 2, y - h // 2)
        else:
            # Si no hay sprite cargado, usar un círculo azul como fallback
            cv2.circle(frame, self.position, self.radius, (255, 0, 0), -1)

    def is_eaten(self, head_pos):
        """
        Verifica si la cabeza de la serpiente ha alcanzado la comida.

        Parámetros:
        - head_pos: Posición actual de la cabeza de la serpiente (tupla x, y)

        Retorna:
        - True si ha sido comida, False en caso contrario.
        """
        if head_pos is None:
            return False
        dist = math.hypot(self.position[0] - head_pos[0], self.position[1] - head_pos[1])
        return dist < self.radius + 10  # Umbral de colisión
