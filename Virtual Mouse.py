import random
import cv2
import mediapipe as mp # Has hand module to detect all points and landmarks on hand
import util
import pyautogui
from pynput.mouse import Button, Controller # Library for clicking tasks

screen_width, screen_height = pyautogui.size()
mouse = Controller()
mpHands = mp.solutions.hands
hands = mpHands.Hands(
    # Confidence is how certain a model is about its prediction
    static_image_mode = False, # Since we are capturing a video
    model_complexity = 1, # Moderate speed and accurate
    min_detection_confidence = 0.7, # Min confidence score to detect the hand in frame is 70%
    min_tracking_confidence = 0.7, # Min confidence score to track the detected hand in frame is 70%
    max_num_hands = 1
)

def find_finger_tip(processed):
    if processed.multi_hand_landmarks :
        hand_landmarks = processed.multi_hand_landmarks[0]
        return hand_landmarks.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP] # Contains the index for the index fingertip
    return None

def move_mouse(index_finger_tip):
    if index_finger_tip is not None:
        # Get x & y coordinate of the index finger relative to the screen width & screen height
        x = int(index_finger_tip.x * screen_width)
        y = int(index_finger_tip.y * screen_height)
        pyautogui.moveTo(x, y) # This function will move the mouse to the x & y coordiates mentioned above

def is_left_click(landmarks_list, thumb_index_dist):
    return (util.get_angle(landmarks_list[5], landmarks_list[6], landmarks_list[8]) < 50
            and util.get_angle(landmarks_list[9], landmarks_list[10], landmarks_list[12]) > 90) and thumb_index_dist > 50
    # Thumb open, index closed and middle finger open

def is_right_click(landmarks_list, thumb_index_dist):
    return (util.get_angle(landmarks_list[5], landmarks_list[6], landmarks_list[8]) > 90
            and util.get_angle(landmarks_list[9], landmarks_list[10], landmarks_list[12]) < 50) and thumb_index_dist > 50
    # Thumb open, index opened and middle finger closed

def is_double_click(landmarks_list, thumb_index_dist):
    return (util.get_angle(landmarks_list[5], landmarks_list[6], landmarks_list[8]) < 50
            and util.get_angle(landmarks_list[9], landmarks_list[10], landmarks_list[12]) < 50) and thumb_index_dist > 50
    # Thumb open, index closed and middle finger closed

def is_screenshot(landmarks_list, thumb_index_dist):
    return (util.get_angle(landmarks_list[5], landmarks_list[6], landmarks_list[8]) < 50
            and util.get_angle(landmarks_list[9], landmarks_list[10], landmarks_list[12]) < 50) and thumb_index_dist < 50
    # All thumb, index and middle finger are closed

def detect_gestures(frame, landmarks_list, processed):
    if len(landmarks_list) >= 21: # Hand contains 21 landmarks though not using all we need all landmarks
        index_finger_tip = find_finger_tip(processed)
        thumb_index_dist = util.get_distance([landmarks_list[4], landmarks_list[5]])
        if thumb_index_dist < 50 and util.get_angle(landmarks_list[6], landmarks_list[6], landmarks_list[8]) > 90:
            # As till 100 so < 50 means thumb moved and angle to check index finger is upright
            move_mouse(index_finger_tip)
        # Left click
        elif is_left_click(landmarks_list, thumb_index_dist):
            mouse.press(Button.left)
            mouse.release(Button.left)
            cv2.putText(frame, "Left Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2) # To put text that your clicking left
        # Right click
        elif is_right_click(landmarks_list, thumb_index_dist):
            mouse.press(Button.right)
            mouse.release(Button.right)
            cv2.putText(frame, "Right Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        # Double click
        elif is_double_click(landmarks_list, thumb_index_dist):
            pyautogui.doubleClick() # Pyatogui is more precise for double click than pynput library
            cv2.putText(frame, "Double Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        # Screenshot
        elif is_screenshot(landmarks_list, thumb_index_dist):
            im1 = pyautogui.screenshot() # The screenshot is stored in a varible named im1
            label = random.randint(1, 1000) # We will take multiple screenshot so to save with different name we use random
            im1.save(f'my_screenshot_{label}.png')
            cv2.putText(frame, "Screenshot Taken", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)


def main():
    cap = cv2.VideoCapture(1) # To open camera and capture video also 0 for single camera
    draw = mp.solutions.drawing_utils # To draw the landmarks

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            # ret returns true if it can capture frames and frames for actually capturing frames
            if not ret:
                break
            frame = cv2.flip(frame, 1) # To show mirror image
            framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # Mediapipe requires frame to be passed in RGB format
            # By default frame captures in BGR format
            processed = hands.process(framergb)

            landmarks_list = []

            if processed.multi_hand_landmarks:
                hand_landmarks = processed.multi_hand_landmarks[0] # Take landmarks from one of the hands
                draw.draw_landmarks(frame, hand_landmarks, mpHands.HAND_CONNECTIONS) # Predefined connections that link 21 handmarks

                for lm in hand_landmarks.landmark:
                    landmarks_list.append((lm.x, lm.y)) # Appending into list the x & y coordinates of landmarks

            detect_gestures(frame, landmarks_list, processed) # To detect gestures and code for mouse actions

            cv2.imshow('Frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('x'):
                break
                # stops recording if we press 'x' where 0xFF for keyobaord and ord is to convert to ASCII

    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
    # This module cannot be imported and run by anyother python file