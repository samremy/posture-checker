import numpy as np
import mediapipe as mp
from PySide6.QtCore import QObject
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.framework.formats import landmark_pb2

class PoseHandler(QObject):
    base_options = python.BaseOptions(model_asset_path="../pose_landmarker.task")
    options = vision.PoseLandmarkerOptions(base_options=base_options, running_mode=vision.RunningMode.VIDEO)
    pose_detector = vision.PoseLandmarker.create_from_options(options)

    def draw_landmarks_on_image(rgb_image, detection_result):
        """
        Draw MediaPipe pose landmarks onto webcam frame
        """
        pose_landmarks_list = detection_result.pose_landmarks
        annotated_image = np.copy(rgb_image)

        for idx in range(len(pose_landmarks_list)):
            pose_landmarks = pose_landmarks_list[idx]

            # Draw the pose landmarks.
            pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
            pose_landmarks_proto.landmark.extend([
                landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in pose_landmarks
            ])
            mp.solutions.drawing_utils.draw_landmarks(
                annotated_image,
                pose_landmarks_proto,
                mp.solutions.pose.POSE_CONNECTIONS,
                mp.solutions.drawing_styles.get_default_pose_landmarks_style())
        return annotated_image

    def get_mp_frame(frame):
        """
        return Image obj usable by MediaPipe
        """
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
        mp_frame = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )
        return mp_frame

    def get_posture_value(detection_result):
        """
        Get normalized distance between nose and center of shoulders
        """
        people_world_landmarks = detection_result.pose_world_landmarks
        if len(people_world_landmarks) == 0:  # No person detected
            return
        wl = people_world_landmarks[0]  # Landmarks of person in frame
        nose = wl[0].y
        shoulder_R = wl[11].y
        shoulder_L = wl[12].y
        shoulder_mid = (shoulder_L + shoulder_R) / 2  # Midpoint height
        return shoulder_mid - nose  # Horizontal Diff