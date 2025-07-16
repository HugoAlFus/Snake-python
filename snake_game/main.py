"""
Autor: Hugo Almodóvar Fuster
Versión: 1.0

Descripción:
Este es el script principal del juego Snake controlado con el dedo índice usando visión por computadora.
Utiliza la cámara web para rastrear la mano del usuario mediante MediaPipe, permitiendo controlar la serpiente.
El juego genera comida, registra la puntuación y guarda los resultados al finalizar.

Dependencias:
- OpenCV
- MediaPipe
"""

import os
import time
from datetime import datetime
import cv2

from food import Food
from snake import Snake
from snake_game.util.hand_tracker import HandTracker

# Inicializa la cámara
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
height, width = frame.shape[:2]

# Instancia de los módulos del juego
tracker = HandTracker()
snake = Snake()
food = Food(width, height)

# Variables de control de tiempo y puntuación
start_time = time.time()
duration = 120  # Duración de la partida en segundos
score = 0


def create_file_match():
    """
    Crea un archivo de texto al finalizar la partida con los datos de score y tiempo.
    Si hay colisión de nombre, añade score y duración al nombre.
    """
    path_base = "../matchs"
    os.makedirs(path_base, exist_ok=True)

    # Nombre base con hora
    base_name = datetime.now().strftime("%H-%M-%S")
    filename = f"{base_name}.txt"
    filepath = os.path.join(path_base, filename)

    # Si ya existe, lo diferencia añadiendo puntuación y tiempo
    if os.path.exists(filepath):
        filename = f"{base_name} Score-{score} Time-{duration}.txt"
        filepath = os.path.join(path_base, filename)

    # Guarda la partida
    with open(filepath, "w") as write_file:
        write_file.write(f"Score: {score}\n")
        write_file.write(f"Time: {duration}")


# Bucle principal del juego
while True:
    ret, frame = cap.read()
    if not ret or frame is None:
        print("❌ Error leyendo de la cámara")
        continue

    # Rastrear dedo índice
    try:
        finger_pos = tracker.get_index_finger_position(frame)
        tracker.draw_hand(frame)  # Dibuja la mano para depuración visual
    except Exception as e:
        print("❌ Error al detectar mano:", e)
        finger_pos = None

    # Actualizar y dibujar serpiente
    if finger_pos:
        snake.update(finger_pos)
    snake.draw(frame)

    # Dibujar comida
    food.draw(frame)

    # Comprobación si fue comida
    if food.is_eaten(snake.get_head()):
        snake.grow()
        food = Food(width, height)
        score += 1

    # Mostrar puntuación y tiempo restante
    elapsed_time = time.time() - start_time
    remaining_time = max(0, int(duration - elapsed_time))

    cv2.putText(frame, f"Score: {score}", (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(frame, f"Time: {remaining_time}s", (10, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Finalizar si se agota el tiempo
    if remaining_time == 0:
        cv2.putText(frame, "GAME OVER", (width // 2 - 200, height // 2),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 4)
        cv2.imshow("Snake con dedo y comida", frame)
        cv2.waitKey(3000)
        create_file_match()
        break

    # Mostrar el juego
    cv2.imshow("Snake con dedo y comida", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Limpieza final
cap.release()
cv2.destroyAllWindows()
