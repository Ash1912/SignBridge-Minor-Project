import cv2 #OpenCV library for computer vision
import numpy as np #Numerical computing library for Python
import os #Provides a way of using operating system dependent functionality
from matplotlib import pyplot as plt #Data visualization library
import time    #Provides various time-related functions
import mediapipe as mp #Medipipe shows the moment
import pyttsx3 #text-to-speech conversion
from mediapipe_utils import *
from tensorflow.keras.models import Sequential #A class from Keras API for creating neural network models in a sequential manner
#Long Short-Term Memory layer for Keras API
from tensorflow.keras.layers import LSTM, Dense #A regular densely connected neural network layer for Keras API
from tensorflow.keras.callbacks import TensorBoard #A visualization toolkit for TensorFlow library
import threading #A module provides a way of creating multiple threads of execution

mp_holistic = mp.solutions.holistic # Holistic model
mp_drawing = mp.solutions.drawing_utils # Drawing utilities
actions = np.array(['hello', 'thanks', 'surprise'])
engine = pyttsx3.init() #An instance of pyttsx3.init() to initialize text-to-speech engine


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

def say_threads(text):
    thread = threading.Thread(target=say, args=(text,))
    thread.start()

def show_window():
    print("loading model...")
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
                    say_threads(sentence[-1])
                    speak_flag = False

                # Viz probabilities
                #image = prob_viz(res, actions, image, colors)

            cv2.rectangle(image, (0, 0), (640, 40), (165, 148, 48), -1)
            cv2.putText(image, ' '.join(sentence), (3, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (55, 11, 11), 2, cv2.LINE_AA)

            # Show to screen
            cv2.imshow('Sign Bridge', image)

            # Break gracefully
            if (cv2.waitKey(10) & 0xFF == ord('q')) or cv2.waitKey(10) & 0xFF == ord('Q'):
                break
        cap.release()
        cv2.destroyAllWindows()
