import cv2
import time

cap = cv2.VideoCapture(0) #0 for default webcam
start_time = time.monotonic()

if not cap.isOpened(): #No webcam handling
    print("Error: No webcam found")
    exit()

def get_frame():
    ret, frame = cap.read()
    if not ret:
        print("Error: No webcam found")
        return None #No webcam found
    return frame

def get_timestamp_ms():
    return int((time.monotonic() - start_time) * 1000)

def get_rgb_frame(bgr_frame):
    rgb_frame = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
    return rgb_frame

def cleanup():
    cap.release()
    cv2.destroyAllWindows()