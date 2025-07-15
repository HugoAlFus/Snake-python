import math
import os

import cv2

from snake_game.util.overlay import overlay_image


class Snake:
    def __init__(self, max_length=30):
        self.body = []
        self.max_length = max_length
        self.current_length = 0
        self.previous_head = None
        self.pending_growth = 0

        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "sprites", "snake"))

        segment_path = os.path.join(base_path, "snake_segment.png")
        head_path = os.path.join(base_path, "snake_head.png")

        print("Cargando segmento desde:", segment_path)
        print("Cargando cabeza desde:", head_path)

        self.segment_image = cv2.imread(segment_path, cv2.IMREAD_UNCHANGED)
        self.head_image = cv2.imread(head_path, cv2.IMREAD_UNCHANGED)

        print("Segment loaded:", self.segment_image is not None)
        print("Head loaded:", self.head_image is not None)

        if self.segment_image is not None:
            self.segment_image = cv2.resize(self.segment_image, (20, 20))

        if self.head_image is not None:
            self.head_image = cv2.resize(self.head_image, (24, 24))

    def update(self, head_pos):
        if self.previous_head is None:
            self.previous_head = head_pos
            self.body.append(head_pos)
            return

        x1, y1 = self.previous_head
        x2, y2 = head_pos
        distance = math.hypot(x2 - x1, y2 - y1)

        steps = int(distance / 8)
        if steps == 0:
            return

        for i in range(1, steps + 1):
            t = i / steps
            x = int(x1 + (x2 - x1) * t)
            y = int(y1 + (y2 - y1) * t)

            self.body.append((x, y))

            if self.pending_growth > 0:
                self.pending_growth -= 1
                self.current_length += 1
            else:
                if self.body:
                    self.body.pop(0)

        self.previous_head = head_pos

        # Limitar longitud
        while len(self.body) > self.max_length:
            self.body.pop(0)

    def draw(self, frame):
        if self.segment_image is None or self.head_image is None:
            # Si no hay imágenes, pinta con líneas y círculos simples (fallback)
            for i in range(1, len(self.body)):
                cv2.line(frame, self.body[i - 1], self.body[i], (0, 255, 0), 10)
            if self.body:
                cv2.circle(frame, self.body[-1], 8, (0, 0, 255), -1)
            return

            # Dibuja segmentos
        for pos in self.body[:-1]:
            x, y = pos
            h, w = self.segment_image.shape[:2]
            overlay_image(frame, self.segment_image, x - w // 2, y - h // 2)

            # Dibuja cabeza
        if self.body:
            x, y = self.body[-1]
            h, w = self.head_image.shape[:2]
            overlay_image(frame, self.head_image, x - w // 2, y - h // 2)

    def grow(self, amount=1):
        self.pending_growth += amount

    def get_head(self):
        return self.body[-1] if self.body else None

    def check_self_collision(self):
        head = self.get_head()
        if not head:
            return False

        for point in self.body[:-10]:
            dist = math.hypot(head[0] - point[0], head[1] - point[1])
            if dist < 10:
                return True
        return False
