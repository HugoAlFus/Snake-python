"""
Autor: Hugo Almodóvar Fuster
Versión: 1.0
Descripción:
Función utilitaria para superponer una imagen PNG con canal alfa (transparencia)
sobre un fondo (por ejemplo, una cámara o escena de juego).
"""

import numpy as np

def overlay_image(background, overlay, x, y):
    """
    Superpone una imagen con transparencia (RGBA) sobre otra (BGR) en la posición (x, y).

    Parámetros:
    - background: Imagen base sobre la cual se va a dibujar (por ejemplo, el frame de la cámara).
    - overlay: Imagen con canal alfa (RGBA), como un sprite con transparencia.
    - x, y: Coordenadas de la esquina superior izquierda donde colocar la imagen superpuesta.

    Retorna:
    - None (modifica directamente la imagen de fondo).
    """

    h, w = overlay.shape[:2]

    # Verificar si la imagen de superposición está dentro de los límites del fondo
    if x < 0 or y < 0 or x + w > background.shape[1] or y + h > background.shape[0]:
        return  # No se dibuja si está fuera del frame

    # Separar canales de color y de alfa
    overlay_rgb = overlay[:, :, :3]          # Canal de color (BGR)
    mask = overlay[:, :, 3:] / 255.0         # Canal alfa normalizado
    inv_mask = 1.0 - mask                    # Máscara inversa para el fondo

    # Extraer región de interés (ROI) del fondo donde se colocará el sprite
    roi = background[y:y + h, x:x + w]

    # Mezclar píxel a píxel usando la máscara alfa
    for c in range(3):  # B, G, R
        roi[:, :, c] = roi[:, :, c] * inv_mask[:, :, 0] + overlay_rgb[:, :, c] * mask[:, :, 0]

    # Colocar el resultado final de nuevo en la imagen de fondo
    background[y:y + h, x:x + w] = roi
