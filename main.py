import cv2
from gtts import gTTS
import os
from cvzone.HandTrackingModule import HandDetector

detector = HandDetector(maxHands=2)

# hand signs to text
def hand_signs_to_text(left_fingers, right_fingers):
    if left_fingers == [1, 1, 1, 1, 1]:
        return 'Hello'
    elif left_fingers == [1, 1, 0, 0, 1]:
        return 'I Love You'
    elif left_fingers == [1, 0, 0, 0, 0]:
        return 'Good'
    elif left_fingers == [0, 1, 1, 0, 0]:
        return 'Peace Out'
    elif left_fingers == [1, 1, 0, 0, 0]:
        return 'Smile'
    elif left_fingers == [0, 1, 1, 1, 1]:
        return 'Thank'
    elif left_fingers == [0, 1, 0, 0, 0]:
        return 'You'
    else:
        return 'um'

# text to speech
def text_to_speech(text):
    tts = gTTS(text=text, lang='en', slow=False)
    tts.save("output.mp3")
    os.system("start output.mp3") 

cap = cv2.VideoCapture(0)

gesture_spoken = False  
current_gesture = None 

while True:
  
    success, frame = cap.read()
    if not success:
        break

    hands, _ = detector.findHands(frame)

    if hands:
        left_hand = hands[0] if len(hands) > 0 else None
        right_hand = hands[1] if len(hands) > 1 else None

        left_fingers = detector.fingersUp(left_hand) if left_hand else [0, 0, 0, 0, 0]
        right_fingers = detector.fingersUp(right_hand) if right_hand else [0, 0, 0, 0, 0]

        new_gesture = hand_signs_to_text(left_fingers, right_fingers)

        if new_gesture != current_gesture:  # check if the gesture has changed
            current_gesture = new_gesture
            text_to_speech(current_gesture)

    cv2.imshow("Hand Gesture to Speech", frame)

    # press 'q' for quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()