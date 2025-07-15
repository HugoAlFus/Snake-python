import math
import os
import random

import cv2

from snake_game.util.overlay import overlay_image


class Food:
    def __init__(self, frame_width, frame_height):
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.radius = 15
        self.position = self._generate_random_position()

        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "sprites", "food"))

        apple_path = os.path.join(base_path, "apple.png")

        self.image = cv2.imread(apple_path, cv2.IMREAD_UNCHANGED)
        if self.image is not None:
            self.image = cv2.resize(self.image, (30, 30))

    def _generate_random_position(self):
        margin = 50
        x = random.randint(margin, self.frame_width - margin)
        y = random.randint(margin, self.frame_height - margin)
        return x, y

    def draw(self, frame):
        if self.image is not None:
            x, y = self.position
            h, w = self.image.shape[:2]
            overlay_image(frame, self.image, x - w // 2, y - h // 2)
        else:
            cv2.circle(frame, self.position, self.radius, (255, 0, 0), -1)

    def is_eaten(self, head_pos):
        if head_pos is None:
            return False
        dist = math.hypot(self.position[0] - head_pos[0], self.position[1] - head_pos[1])
        return dist < self.radius + 10
