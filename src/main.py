import cv2
import time
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.framework.formats import landmark_pb2


#Define Constants
START_TIME = time.time() #Time on init


#Mediapipe Setup
base_options = python.BaseOptions(model_asset_path="../pose_landmarker.task")
options = vision.PoseLandmarkerOptions(base_options=base_options, running_mode=vision.RunningMode.VIDEO)
pose_detector = vision.PoseLandmarker.create_from_options(options)


#Webcam Setup
cap = cv2.VideoCapture(0) #0 for default webcam
if not cap.isOpened(): #No webcam handling
    print("Error: No webcam found")
    exit()


#Posture to overwrite
default_posture_value = 1
sensitivity = 0.75


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
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #Convert BGR to RGB
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
    if len(people_world_landmarks) == 0: #No person detected
        return
    wl = people_world_landmarks[0] #Landmarks of person in frame
    nose = wl[0].y
    shoulder_R = wl[11].y
    shoulder_L = wl[12].y
    shoulder_mid = (shoulder_L + shoulder_R) / 2 #Midpoint height
    return shoulder_mid - nose #Horizontal Diff


#Running loop
while True:
    ret, frame = cap.read()
    if not ret:
        break

    timestamp_ms = int((time.time() - START_TIME) * 1000) #Time since init in ms
    mp_frame = get_mp_frame(frame)
    detection_result = pose_detector.detect_for_video(mp_frame, timestamp_ms=timestamp_ms)

    if cv2.waitKey(1) & 0xFF == ord('s'): #Set default value on s keypress
        default_posture_value = get_posture_value(detection_result)

    elif default_posture_value != 1: #Default posture has been set
        posture_value = get_posture_value(detection_result)
        if posture_value <= default_posture_value * sensitivity:
            pass #Bad Posture
        else:
            pass #Good Posture

    frame_with_landmarks = draw_landmarks_on_image(frame.copy(), detection_result)
    cv2.imshow("Pose Detection", frame_with_landmarks)

    #Break on "q" keypress
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# Cleanup
cap.release()
cv2.destroyAllWindows()