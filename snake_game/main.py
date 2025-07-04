import cv2
from hand_tracker import HandTracker
from snake import Snake
from food import Food

# Inicializar cámara
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
height, width = frame.shape[:2]

tracker = HandTracker()
snake = Snake()
food = Food(width, height)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Obtener dedo
    finger_pos = tracker.get_index_finger_position(frame)
    tracker.draw_hand(frame)

    # Serpiente
    if finger_pos:
        snake.update(finger_pos)
    snake.draw(frame)

    # Comida
    food.draw(frame)

    # Verificar si fue comida
    if food.is_eaten(snake.get_head()):
        snake.grow()
        food = Food(width, height)  # nueva comida

    # Mostrar
    cv2.imshow("Snake con dedo y comida", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
