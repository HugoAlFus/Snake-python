import cv2
import numpy as np

# Manzana (food.png)
apple = np.zeros((30, 30, 4), dtype=np.uint8)
cv2.circle(apple, (15, 18), 12, (0, 0, 255, 255), -1)        # rojo manzana
cv2.rectangle(apple, (13, 3), (17, 10), (0, 255, 0, 255), -1) # tallo verde
cv2.imwrite("../../assets/sprites/food/apple.png", apple)

# Segmento cuerpo serpiente (snake_segment.png)
segment = np.zeros((20, 20, 4), dtype=np.uint8)
cv2.circle(segment, (10, 10), 9, (0, 150, 0, 255), -1)       # verde oscuro cuerpo
cv2.imwrite("../../assets/sprites/snake/snake_segment.png", segment)

# Cabeza serpiente (snake_head.png)
head = np.zeros((24, 24, 4), dtype=np.uint8)
cv2.circle(head, (12, 12), 11, (0, 200, 0, 255), -1)          # verde claro cabeza

# Ojos negros con brillo blanco
cv2.circle(head, (7, 8), 3, (0, 0, 0, 255), -1)             # ojo izquierdo negro
cv2.circle(head, (7, 8), 1, (255, 255, 255, 255), -1)       # brillo ojo
cv2.circle(head, (17, 8), 3, (0, 0, 0, 255), -1)            # ojo derecho negro
cv2.circle(head, (17, 8), 1, (255, 255, 255, 255), -1)      # brillo ojo

cv2.imwrite("../../assets/sprites/snake/snake_head.png", head)
