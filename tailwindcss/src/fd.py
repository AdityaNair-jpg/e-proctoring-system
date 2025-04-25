import cv2
import mediapipe as mp
import time
import datetime
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from collections import deque
import requests
import os

# Initialize MediaPipe
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

# Constants for Eye Tracking
LEFT_EYE = [33, 133]
RIGHT_EYE = [362, 263]

# Suspicious Activity Threshold
LOOK_AWAY_THRESHOLD = 3

# Initialize Video Capture
cap = cv2.VideoCapture(0)

# Track suspicious activity
look_away_counter = 0
suspicious_events = []
session_start_time = datetime.datetime.now()

# Data for plotting
suspicion_levels = deque(maxlen=1000)
time_stamps = deque(maxlen=1000)
start_time = time.time()

# Set up live plot
fig, ax = plt.subplots()
line, = ax.plot([], [], 'r-', label='Suspicion Level')
ax.set_xlim(0, 60)
ax.set_ylim(0, 10)
ax.set_xlabel('Time (s)')
ax.set_ylabel('Suspicion Level')
ax.legend()

def update_plot(frame):
    ax.set_xlim(max(0, time.time() - start_time - 60), time.time() - start_time)
    line.set_data(time_stamps, suspicion_levels)
    return line,

ani = animation.FuncAnimation(fig, update_plot, interval=500)
plt.ion()
plt.show()

# Face Mesh Model
with mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
) as face_mesh:

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_frame)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                mp_drawing.draw_landmarks(
                    frame, face_landmarks, mp_face_mesh.FACEMESH_TESSELATION,
                    mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=0, circle_radius=1))

                h, w, _ = frame.shape
                left_eye = face_landmarks.landmark[LEFT_EYE[0]]
                right_eye = face_landmarks.landmark[RIGHT_EYE[0]]

                left_eye_x = int(left_eye.x * w)
                right_eye_x = int(right_eye.x * w)
                left_eye_y = int(left_eye.y * h)
                right_eye_y = int(right_eye.y * h)

                face_center_x = (left_eye_x + right_eye_x) // 2
                face_center_y = (left_eye_y + right_eye_y) // 2
                frame_center_x = w // 2
                frame_center_y = h // 2

                offset_x = abs(face_center_x - frame_center_x)
                offset_y = abs(face_center_y - frame_center_y)

                if offset_x > w * 0.035 or offset_y > h * 0.015:
                    look_away_counter += 1
                else:
                    look_away_counter = 0

                if look_away_counter >= LOOK_AWAY_THRESHOLD:
                    alert_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    suspicious_events.append(f"{alert_time}: Suspicious Activity Detected")
                    cv2.putText(frame, 'ALERT: Suspicious Activity Detected!', (30, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        suspicion_levels.append(look_away_counter)
        time_stamps.append(time.time() - start_time)

        plt.draw()
        plt.pause(0.001)

        cv2.imshow('E-Proctoring System', frame)

        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

# Session End
session_end_time = datetime.datetime.now()
cap.release()
cv2.destroyAllWindows()

# Send report to backend
try:
    response = requests.post("http://localhost:5000/save_report", json={
        "session_start": str(session_start_time),
        "session_end": str(session_end_time),
        "suspicious_events": suspicious_events,
        "timestamps": list(time_stamps),
        "suspicion_levels": list(suspicion_levels)
    })
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Report successfully saved to backend!")
        print(f"📝 PDF: {data['pdf']}")
        print(f"📈 Graph: {data['graph']}")
    else:
        print("❌ Failed to save report to backend.", response.text)
except Exception as e:
    print(f"❌ Error sending report to backend: {e}")
