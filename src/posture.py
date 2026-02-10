import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

default_posture_value = 0
sensitivity = 75 / 100

options = vision.PoseLandmarkerOptions(
    base_options=python.BaseOptions(model_asset_path="pose_landmarker.task"),
    running_mode=vision.RunningMode.VIDEO,
    output_segmentation_masks=False
)
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
        print("Error: No person in frame")
        return 0
    wl = people_world_landmarks[0]  # Landmarks of person in frame
    nose = wl[0].y
    shoulder_R = wl[11].y
    shoulder_L = wl[12].y
    shoulder_mid = (shoulder_L + shoulder_R) / 2  # Midpoint height
    posture_value = shoulder_mid - nose # Horizontal Diff
    return posture_value

def draw_landmarks_on_image(rgb_image, detection_result):
    pose_landmarks_list = detection_result.pose_landmarks
    annotated_image = np.copy(rgb_image)

    pose_landmark_style = vision.drawing_styles.get_default_pose_landmarks_style()
    pose_connection_style = vision.drawing_utils.DrawingSpec(color=(0, 255, 0), thickness=2)

    for pose_landmarks in pose_landmarks_list:
        vision.drawing_utils.draw_landmarks(
            image=annotated_image,
            landmark_list=pose_landmarks,
            connections=vision.PoseLandmarksConnections.POSE_LANDMARKS,
            landmark_drawing_spec=pose_landmark_style,
            connection_drawing_spec=pose_connection_style
        )

    return annotated_image

def cleanup():
    pose_detector.close()

