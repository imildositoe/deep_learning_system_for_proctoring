import numpy as np
import cv2
import os
import librosa
from gt_preparation import gt_file_to_dict

"""
Function to extract frames from the webcam video and return the number of cheating segments
"""
def extract_frames_for_segments(video_path, segments, resize=(224, 224)):
    capture = cv2.VideoCapture(video_path)
    if not capture.isOpened():
        raise Exception(f"Failure opening the video: {video_path}")
    
    total_frames = capture.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = capture.get(cv2.CAP_PROP_FPS)
    print("Frame count: ", total_frames, "\nFPS: ", fps)

    segment_frames = []

    for segment in segments:
        start_frame = int(segment["start_time_in_sec"] * fps)
        end_frame = int(segment["end_time_in_sec"] * fps)
        cheating_type = segment["cheating_type"]

        capture.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        frames = []

        for f in range(start_frame, min(end_frame, total_frames)):
            ret, frame = capture.read()
            if not ret:
                break
            if resize:
                frame = cv2.resize(frame, resize)
            frames.append(frame)

        segment_frames.append({
            "frames": frames,
            "label": cheating_type
        })
    
    capture.release()
    return segment_frames

# Printing the nr of cheating segments in the video
segments = gt_file_to_dict(os.path.join(r'C:\Users\Dell 88\Desktop\OEP database\subject1', 'gt.txt'))
video_path = r'C:\Users\Dell 88\Desktop\OEP database\subject1\Yousef1.avi'
video_segments = extract_frames_for_segments(video_path, segments)
print(f"Extracted {len(video_segments)} video segments")


"""
Function to extract MFCC audio features
"""
def extract_mfcc_for_segments(audio_path, segments, sr=22050, n_mfcc=13):
    y, sr = librosa.load(audio_path, sr=sr)
    duration_sec = librosa.get_duration(y=y, sr=sr)
    print(f"The audio: {audio_path} has a duraction of {duration_sec} seconds and a sampling rate of {sr}")

    segment_audios = []

    for segment in segments:
        start_sample = int(segment["start_time_in_sec"] * sr)
        end_sample = int(segment["end_time_in_sec"] * sr)
        cheating_type = segment["cheating_type"]

        if end_sample > len(y):
            end_sample = len(y)

        y_segment = y[start_sample:end_sample]
        # To handle too short segments
        if len(y_segment) < sr * 0.5:
            continue

        mfcc = librosa.feature.mfcc(y=y_segment, sr=sr, n_mfcc=n_mfcc)
        segment_audios.append({
            "mfcc": mfcc,
            "label": cheating_type
        })

    return segment_audios

# Printing the nr of extracted audio segments
audio_path = r'C:\Users\Dell 88\Desktop\OEP database\subject1\Yousef.wav'
audio_segments = extract_mfcc_for_segments(audio_path, segments)
print(f"Extracted {len(audio_segments)} audio segments")