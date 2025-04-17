
import cv2
import mediapipe as mp
import numpy as np
import time

# Initialize Mediapipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8)
mp_draw = mp.solutions.drawing_utils

# Start webcam
cap = cv2.VideoCapture(0)

# Get the initial frame size from the webcam
ret, frame = cap.read()
if not ret:
    print("Failed to access webcam")
    cap.release()
    exit()

frame_height, frame_width, _ = frame.shape
canvas = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)

# Drawing settings
colors = [(0, 0, 255), (0, 255, 0), (255, 0, 0), (0, 255, 255)]  # Red, Green, Blue, Yellow
color_index = 0  # Start with Red
draw_color = colors[color_index]
thickness = 5

prev_x, prev_y = None, None  # Previous finger position
history = []  # Stores drawn lines for undo feature

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # Flip for mirror effect
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with Mediapipe
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            landmarks = hand_landmarks.landmark

            # Get finger positions
            h, w, _ = frame.shape
            index_x, index_y = int(landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * w), \
                               int(landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * h)
            middle_x, middle_y = int(landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x * w), \
                                 int(landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y * h)
            ring_x, ring_y = int(landmarks[mp_hands.HandLandmark.RING_FINGER_TIP].x * w), \
                             int(landmarks[mp_hands.HandLandmark.RING_FINGER_TIP].y * h)

            # Count raised fingers
            fingers = []
            for i, tip in enumerate([mp_hands.HandLandmark.INDEX_FINGER_TIP,
                                     mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
                                     mp_hands.HandLandmark.RING_FINGER_TIP]):
                if landmarks[tip].y < landmarks[tip - 2].y:  # Compare tip with knuckle
                    fingers.append(i)

            # If only index finger is up → Draw
            if len(fingers) == 1 and 0 in fingers:
                if prev_x is not None and prev_y is not None:
                    cv2.line(canvas, (prev_x, prev_y), (index_x, index_y), draw_color, thickness)
                    history.append(((prev_x, prev_y), (index_x, index_y), draw_color, thickness))

                prev_x, prev_y = index_x, index_y

            else:
                prev_x, prev_y = None, None  # Reset if finger is lifted

            # If index + middle fingers are up → Change color
            if len(fingers) == 2 and 0 in fingers and 1 in fingers:
                color_index = (color_index + 1) % len(colors)
                draw_color = colors[color_index]
                time.sleep(0.3)  # Prevent rapid switching

            # If three fingers are up → Undo last stroke
            if len(fingers) == 3:
                if history:
                    history.pop()  # Remove last drawn line
                    canvas = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)
                    for line in history:
                        cv2.line(canvas, line[0], line[1], line[2], line[3])
                time.sleep(0.3)  # Prevent rapid undo

            # Draw hand landmarks
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Resize canvas to match frame size before blending
    canvas_resized = cv2.resize(canvas, (frame.shape[1], frame.shape[0]))
    frame = cv2.addWeighted(frame, 0.5, canvas_resized, 0.5, 0)

    # Display the active color in the corner
    cv2.rectangle(frame, (10, 10), (60, 60), draw_color, -1)

    # Show the output
    cv2.imshow("Air Canvas", frame)

    # Key controls
    key = cv2.waitKey(1)
    if key == ord('c'):  # Press 'c' to clear canvas
        canvas = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)
        history.clear()
    elif key == ord('s'):  # Press 's' to save the drawing
        cv2.imwrite("drawing_output.png", canvas)
        print("Drawing saved as drawing_output.png!")
    elif key == 27:  # Press 'Esc' to exit
        break

cap.release()
cv2.destroyAllWindows()