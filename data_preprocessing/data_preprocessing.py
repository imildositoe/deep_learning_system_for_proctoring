import os
import numpy as np
import librosa
import cv2
import pickle
from tqdm import tqdm
from sklearn.model_selection import train_test_split

DATA_DIR = r'C:\Users\Dell 88\Desktop\OEP database'
OUTPUT_TRAIN_FILE = "data/train_data.pkl"
OUTPUT_TEST_FILE = "data/test_data.pkl"
FRAME_SIZE = (224, 2240)
SEQUENCE_LEN = 10
AUDIO_SR = 22050
MFCC_SIZE = 100
TEST_SPLIT = 0.2
AUDIO_DURATION = 2

def extract_frames(video_path, seq_len=FRAME_SIZE):
    cap = cv2.VideoCapture(video_path)
    frames = []

    while len(frames) < seq_len:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.resize(frame, FRAME_SIZE)
        frames.append(frame)
    cap.release()
    if len(frames) == seq_len:
        return np.array(frames)
    return None

