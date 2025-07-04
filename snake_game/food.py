import math
import random

import cv2


class Food:
    def __init__(self, frame_width, frame_height):
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.radius = 15
        self.position = self._generate_random_position()

    def _generate_random_position(self):
        margin = 50  # para que no aparezca en el borde
        x = random.randint(margin, self.frame_width - margin)
        y = random.randint(margin, self.frame_height - margin)
        return x, y

    def draw(self, frame):
        cv2.circle(frame, self.position, self.radius, (255, 0, 0), -1)

    def is_eaten(self, head_pos):
        if head_pos is None:
            return False
        dist = math.hypot(self.position[0] - head_pos[0], self.position[1] - head_pos[1])
        return dist < self.radius + 10
