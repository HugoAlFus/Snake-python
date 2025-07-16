"""
Autor: Hugo Almodóvar Fuster
Versión: 1.0
Descripción:
Este script genera y guarda imágenes con fondo transparente (canal alfa) que se utilizan como recursos gráficos
en el juego de la serpiente controlado con la mano. Incluye:

- Una manzana (comida) en formato PNG con transparencia
- Un segmento del cuerpo de la serpiente
- La cabeza de la serpiente con ojos
"""

import cv2
import numpy as np

# Crear una imagen vacía de 30x30 con 4 canales (RGBA) para la manzana
apple = np.zeros((30, 30, 4), dtype=np.uint8)

# Dibujar la manzana como un círculo rojo
cv2.circle(apple, (15, 18), 12, (0, 0, 255, 255), -1)  # (x, y), radio, color RGBA

# Dibujar el tallo como un rectángulo verde
cv2.rectangle(apple, (13, 3), (17, 10), (0, 255, 0, 255), -1)

# Guardar la imagen de la manzana en la ruta correspondiente
cv2.imwrite("../../assets/sprites/food/apple.png", apple)

# Crear imagen del segmento del cuerpo de la serpiente (20x20 RGBA)
segment = np.zeros((20, 20, 4), dtype=np.uint8)

# Dibujar el segmento como un círculo verde oscuro
cv2.circle(segment, (10, 10), 9, (0, 150, 0, 255), -1)

# Guardar el segmento del cuerpo
cv2.imwrite("../../assets/sprites/snake/snake_segment.png", segment)

# Crear imagen de la cabeza de la serpiente (24x24 RGBA)
head = np.zeros((24, 24, 4), dtype=np.uint8)

# Dibujar la cabeza como un círculo verde claro
cv2.circle(head, (12, 12), 11, (0, 200, 0, 255), -1)

# Dibujar los ojos (negros con brillo blanco)
# Ojo izquierdo
cv2.circle(head, (7, 8), 3, (0, 0, 0, 255), -1)
cv2.circle(head, (7, 8), 1, (255, 255, 255, 255), -1)

# Ojo derecho
cv2.circle(head, (17, 8), 3, (0, 0, 0, 255), -1)
cv2.circle(head, (17, 8), 1, (255, 255, 255, 255), -1)

# Guardar la cabeza de la serpiente
cv2.imwrite("../../assets/sprites/snake/snake_head.png", head)
