import cv2
import json
import mediapipe as mp
from read_config import read_config
import os

def extract_hand_keypoints(img_path):
    # Initialize MediaPipe Hands
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=True, max_num_hands=2)
    mp_drawing = mp.solutions.drawing_utils
    
    # Read the image
    image = cv2.imread(img_path)
    if image is None:
        raise ValueError("Image not found or unable to read the image file.")
    
    # Convert the BGR image to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Process the image to detect hands
    results = hands.process(image_rgb)
    
    keypoints = []
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            for landmark in hand_landmarks.landmark:
                # Convert normalized coordinates to pixel values
                h, w, _ = image.shape
                x = float(landmark.x * w)
                y = float(landmark.y * h)
                keypoints.append((x, y))
    
    # Release the MediaPipe resources
    hands.close()
    return keypoints, image

def get_file_names(folder_path=""):
    names = os.listdir(folder_path)
    return names

def save_json(m, path):
    with open(path, 'w') as f:
        json.dump(m, f)
    print('saved', path)

def mph_pred_folder():
    folder = read_config()
    # print(img_dir)
    # get file names
    names = get_file_names(folder)
    out = {}
    n = len(names)
    for i, name in enumerate(names):
        print(f'{i}/{n}')
        path = os.path.join(folder, name)
        keypoints, img = extract_hand_keypoints(path)
        key = name
        value = keypoints
        out[key] = value
    save_json(out, 'mph_keypoints.json')

def test():
    mph_pred_folder()

if __name__ == '__main__':
    # test()
    mph_pred_folder()
