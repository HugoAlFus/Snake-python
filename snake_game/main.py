import os
import time
from datetime import datetime
import cv2

from food import Food
from snake import Snake
from snake_game.util.hand_tracker import HandTracker

# Inicializar cámara
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
height, width = frame.shape[:2]

tracker = HandTracker()
snake = Snake()
food = Food(width, height)

start_time = time.time()
duration = 10  # segundos
score = 0


def create_file_match():
    path_base = "../matchs"
    os.makedirs(path_base, exist_ok=True)

    # Base filename con hora
    base_name = datetime.now().strftime("%H-%M-%S")
    filename = f"{base_name}.txt"
    filepath = os.path.join(path_base, filename)

    # Si ya existe, añadir score y tiempo para diferenciarlo
    if os.path.exists(filepath):
        filename = f"{base_name} Score-{score} Time-{duration}.txt"
        filepath = os.path.join(path_base, filename)

    # Guardar archivo
    with open(filepath, "w") as write_file:
        write_file.write(f"Score: {score}\n")
        write_file.write(f"Time: {duration}")



while True:
    ret, frame = cap.read()
    if not ret or frame is None:
        print("❌ Error leyendo de la cámara")
        continue

    # Intentar obtener posición del dedo
    try:
        finger_pos = tracker.get_index_finger_position(frame)
        tracker.draw_hand(frame)
    except Exception as e:
        print("❌ Error al detectar mano:", e)
        finger_pos = None

    # Serpiente
    if finger_pos:
        snake.update(finger_pos)
    snake.draw(frame)

    # Comida
    food.draw(frame)

    # Verificar si fue comida
    if food.is_eaten(snake.get_head()):
        snake.grow()
        food = Food(width, height)
        score += 1

    # Tiempo y puntaje
    elapsed_time = time.time() - start_time
    remaining_time = max(0, int(duration - elapsed_time))

    cv2.putText(frame, f"Score: {score}", (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(frame, f"Time: {remaining_time}s", (10, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    if remaining_time == 0:
        cv2.putText(frame, "GAME OVER", (width // 2 - 200, height // 2),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 4)
        cv2.imshow("Snake con dedo y comida", frame)
        cv2.waitKey(3000)
        create_file_match()
        break

    cv2.imshow("Snake con dedo y comida", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
