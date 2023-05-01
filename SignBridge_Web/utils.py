import cv2
import numpy as np
import os
from matplotlib import pyplot as plt
import time
import mediapipe as mp
import pyttsx3
from mediapipe_utils import *
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.callbacks import TensorBoard
import threading

mp_holistic = mp.solutions.holistic # Holistic model
mp_drawing = mp.solutions.drawing_utils # Drawing utilities
actions = np.array(['hello', 'thanks', 'i love you'])
engine = pyttsx3.init()


def load_model():
    model = Sequential()
    model.add(LSTM(64, return_sequences=True, activation='relu', input_shape=(30,1662)))
    model.add(LSTM(128, return_sequences=True, activation='relu'))
    model.add(LSTM(64, return_sequences=False, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(actions.shape[0], activation='softmax'))
    model.load_weights('action2.h5')

    return model

def say(text):
    engine.say(text)
    engine.runAndWait()
<<<<<<< HEAD

def say_threads(text):
=======
    
def say_in_thread(text):
>>>>>>> fe60e39f95419d7a7f64fa63ccd2f0d8ff46b4ec
    thread = threading.Thread(target=say, args=(text,))
    thread.start()

def show_window():
    print("here")
    sequence = []
    sentence = []
    predictions = []
    threshold = 0.8
    speak_flag = False
    model = load_model()

    cap = cv2.VideoCapture(0)
    # Set mediapipe model
    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        while cap.isOpened():

            # Read feed
            ret, frame = cap.read()

            # Make detections
            image, results = mediapipe_detection(frame, holistic)
            print(results)

            # Draw landmarks
            draw_styled_landmarks(image, results, mp_drawing, mp_holistic)

            # 2. Prediction logic
            keypoints = extract_keypoints(results)
            sequence.append(keypoints)
            sequence = sequence[-30:]

            if len(sequence) == 30:
                res = model.predict(np.expand_dims(sequence, axis=0))[0]
                print(actions[np.argmax(res)])
                predictions.append(np.argmax(res))

                # 3. Viz logic
                if np.unique(predictions[-10:])[0] == np.argmax(res) and res[np.argmax(res)] > threshold:
                    new_action = actions[np.argmax(res)]
                    if len(sentence) > 0:
                        if new_action != sentence[-1]:
                            sentence.append(new_action)
                            if not speak_flag:
                                speak_flag = True
                    else:
                        sentence.append(new_action)
                        if not speak_flag:
                            speak_flag = True

                if len(sentence) > 1:
                    sentence = sentence[-1:]

                # Speak the new action only once
                if speak_flag:
<<<<<<< HEAD
                    say_threads(sentence[-1])
=======
                    say_in_thread(sentence[-1])
>>>>>>> fe60e39f95419d7a7f64fa63ccd2f0d8ff46b4ec
                    speak_flag = False

                # Viz probabilities
                #image = prob_viz(res, actions, image, colors)

            cv2.rectangle(image, (0, 0), (640, 40), (165, 148, 48), -1)
            cv2.putText(image, ' '.join(sentence), (3, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (55, 11, 11), 2, cv2.LINE_AA)

            # Show to screen
            cv2.imshow('OpenCV Feed', image)

            # Break gracefully
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
