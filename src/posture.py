import time
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.framework.formats import landmark_pb2

default_posture_value = 0
sensitivity = 0

base_options = python.BaseOptions(model_asset_path="../pose_landmarker.task")
options = vision.PoseLandmarkerOptions(base_options=base_options, running_mode=vision.RunningMode.VIDEO)
pose_detector = vision.PoseLandmarker.create_from_options(options)

def get_detection_result(mp_frame, timestamp_ms):
    detection_result = pose_detector.detect_for_video(mp_frame, timestamp_ms=timestamp_ms)
    return detection_result

def get_mp_frame(rgb_frame):
    mp_frame = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb_frame
    )
    return mp_frame

def get_posture_value(detection_result):
    people_world_landmarks = detection_result.pose_world_landmarks
    if len(people_world_landmarks) == 0:  # No person detected
        return
    wl = people_world_landmarks[0]  # Landmarks of person in frame
    nose = wl[0].y
    shoulder_R = wl[11].y
    shoulder_L = wl[12].y
    shoulder_mid = (shoulder_L + shoulder_R) / 2  # Midpoint height
    posture_value = shoulder_mid - nose # Horizontal Diff
    print(f"posture_value {posture_value}")
    return posture_value