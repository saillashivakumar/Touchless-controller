import cv2
import time

from hand_tracking import HandTracker
from gestures import get_finger_states, recognize_gesture
from actions import (
    volume_up,
    volume_down,
    play_pause,
    move_cursor_from_hand
)


def main():

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    tracker = HandTracker()

    print("Touchless Controller started.")
    print("Press Q to quit.")

     

    ACTION_COOLDOWN = 0.5

    last_action_time = 0

     

    OPEN_PALM_HOLD_TIME = 1.5

    open_palm_start_time = None
    open_palm_triggered = False

     

    GESTURE_CONFIRM_FRAMES = 3

    previous_gesture = None
    gesture_count = 0
    confirmed_gesture = None

    try:

        while True:

            success, frame = cap.read()

            if not success:
                print("Error: Could not read camera frame.")
                break

             
            frame = cv2.flip(frame, 1)

            
            tracker.process(frame)

            result = tracker.latest_result

            if result and result.hand_landmarks:

                landmarks = result.hand_landmarks[0]

               

                detected_gesture = recognize_gesture(
                    landmarks
                )

                current_time = time.time()

                 

                if detected_gesture == previous_gesture:

                    gesture_count += 1

                else:

                    previous_gesture = detected_gesture
                    gesture_count = 1

                if gesture_count >= GESTURE_CONFIRM_FRAMES:

                    confirmed_gesture = detected_gesture

                 

                if detected_gesture == "INDEX":

                    move_cursor_from_hand(
                        landmarks[8].x,
                        landmarks[8].y
                    )

                

                if (
                    current_time - last_action_time
                    >= ACTION_COOLDOWN
                ):

                    if confirmed_gesture == "THUMB_UP":

                        volume_up()

                        last_action_time = current_time

                    elif confirmed_gesture == "THUMB_DOWN":

                        volume_down()

                        last_action_time = current_time

                 

                if confirmed_gesture == "OPEN_PALM":

                    if open_palm_start_time is None:

                        open_palm_start_time = current_time

                    palm_hold_time = (
                        current_time
                        - open_palm_start_time
                    )

                    if (
                        palm_hold_time >= OPEN_PALM_HOLD_TIME
                        and not open_palm_triggered
                    ):

                        play_pause()

                        open_palm_triggered = True

                else:

                    open_palm_start_time = None
                    open_palm_triggered = False

                

                cv2.putText(
                    frame,
                    f"Gesture: {detected_gesture}",
                    (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    frame,
                    f"Confirmed: {confirmed_gesture}",
                    (20, 90),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (255, 255, 0),
                    2
                )

            else:

                

                previous_gesture = None
                gesture_count = 0
                confirmed_gesture = None

                open_palm_start_time = None
                open_palm_triggered = False

            # Draw detected hand
            frame = tracker.draw_landmarks(frame)

            cv2.imshow(
                "Touchless Controller - Hand Tracking",
                frame
            )

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:

        tracker.close()
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()