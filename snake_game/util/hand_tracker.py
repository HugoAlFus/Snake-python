"""
Autor: Hugo Almodóvar Fuster
Versión: 1.0
Descripción:
Este módulo define una clase `HandTracker` que utiliza MediaPipe para detectar y rastrear una mano
en tiempo real desde una cámara. Se utiliza para controlar la dirección de la serpiente con el dedo índice.
"""

import cv2
import mediapipe as mp


class HandTracker:
    def __init__(self, max_hands=1, detection_confidence=0.7, tracking_confidence=0.7):
        """
        Inicializa el detector de manos usando MediaPipe.

        Parámetros:
        - max_hands: Número máximo de manos a detectar.
        - detection_confidence: Umbral de confianza para la detección inicial.
        - tracking_confidence: Umbral de confianza para el seguimiento.
        """
        self.hands_module = mp.solutions.hands  # Módulo de manos de MediaPipe

        # Crear el objeto de detección y seguimiento de manos
        self.hands = self.hands_module.Hands(
            max_num_hands=max_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )

        self.drawing = mp.solutions.drawing_utils  # Utilidad para dibujar la mano

    def get_index_finger_position(self, frame):
        """
        Devuelve la posición (x, y) del dedo índice si se detecta una mano.

        Parámetro:
        - frame: Imagen en formato BGR capturada desde la cámara.

        Retorna:
        - (x, y): Coordenadas del dedo índice en píxeles, o None si no se detecta.
        """
        # Convertir a RGB (MediaPipe requiere formato RGB)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Procesar el frame para detectar manos
        results = self.hands.process(rgb_frame)

        # Si hay manos detectadas, obtener la primera
        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            h, w, _ = frame.shape

            # Obtener la coordenada del dedo índice
            index_finger_tip = hand_landmarks.landmark[self.hands_module.HandLandmark.INDEX_FINGER_TIP]
            cx, cy = int(index_finger_tip.x * w), int(index_finger_tip.y * h)
            return (cx, cy)

        return None  # No se detectó mano

    def draw_hand(self, frame):
        """
        Dibuja las conexiones de la mano detectada sobre el frame.

        Parámetro:
        - frame: Imagen en formato BGR capturada desde la cámara.

        Retorna:
        - El frame con las manos dibujadas (si se detectan).
        """
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.drawing.draw_landmarks(frame, hand_landmarks, self.hands_module.HAND_CONNECTIONS)

        return frame
