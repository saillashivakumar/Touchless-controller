import cv2
import mediapipe as mp
import time

from mediapipe.tasks import python
from mediapipe.tasks.python import vision


class HandTracker:

    def __init__(self, model_path="models/hand_landmarker.task"):

        base_options = python.BaseOptions(
            model_asset_path=model_path
        )

        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.LIVE_STREAM,
            num_hands=1,
            min_hand_detection_confidence=0.7,
            min_hand_presence_confidence=0.7,
            min_tracking_confidence=0.7,
            result_callback=self._result_callback
        )

        self.landmarker = vision.HandLandmarker.create_from_options(
            options
        )

        self.latest_result = None

    def _result_callback(self, result, output_image, timestamp_ms):
        self.latest_result = result

    def process(self, frame):

        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        timestamp_ms = int(time.time() * 1000)

        self.landmarker.detect_async(
            mp_image,
            timestamp_ms
        )

        return frame

    def draw_landmarks(self, frame):

        if self.latest_result is None:
            return frame

        if not self.latest_result.hand_landmarks:
            return frame

        height, width, _ = frame.shape

        for hand in self.latest_result.hand_landmarks:

            points = []

            for landmark in hand:

                x = int(landmark.x * width)
                y = int(landmark.y * height)

                points.append((x, y))

                cv2.circle(
                    frame,
                    (x, y),
                    5,
                    (0, 255, 0),
                    -1
                )

            # Hand connections
            for connection in vision.HandLandmarksConnections.HAND_CONNECTIONS:

                start = connection.start
                end = connection.end

                cv2.line(
                    frame,
                    points[start],
                    points[end],
                    (0, 255, 0),
                    2
                )

        return frame

    def close(self):

        self.landmarker.close()