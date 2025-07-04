import math
import cv2

class Snake:
    def __init__(self, max_length=150):
        self.body = []
        self.max_length = max_length
        self.current_length = 0
        self.previous_head = None

    def update(self, head_pos):
        if self.previous_head is None:
            self.previous_head = head_pos
            self.body.append(head_pos)
            return

        x1, y1 = self.previous_head
        x2, y2 = head_pos
        distance = math.hypot(x2 - x1, y2 - y1)

        steps = int(distance / 2)
        if steps == 0:
            return

        for i in range(1, steps + 1):
            t = i / steps
            x = int(x1 + (x2 - x1) * t)
            y = int(y1 + (y2 - y1) * t)
            self.body.append((x, y))
            self.current_length += 1

            if self.current_length > self.max_length:
                self.body.pop(0)
                self.current_length -= 1

        self.previous_head = head_pos

    def draw(self, frame):
        for i in range(1, len(self.body)):
            cv2.line(frame, self.body[i - 1], self.body[i], (0, 255, 0), 10)
        if self.body:
            cv2.circle(frame, self.body[-1], 8, (0, 0, 255), -1)

    def grow(self, amount=20):
        self.max_length += amount

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
