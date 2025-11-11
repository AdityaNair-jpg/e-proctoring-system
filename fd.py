import cv2
import mediapipe as mp
import time
import datetime
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from collections import deque

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
suspicious_events = []  # Store detected events
session_start_time = datetime.datetime.now()

# Data for live plotting
suspicion_levels = deque(maxlen=100)
time_stamps = deque(maxlen=100)
start_time = time.time()

# Set up the live plot
fig, ax = plt.subplots()
x_data, y_data = [], []
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
with mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5) as face_mesh:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            break

        # Flip the frame for natural interaction
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Face Mesh Detection
        results = face_mesh.process(rgb_frame)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # Draw landmarks
                mp_drawing.draw_landmarks(
                    frame, face_landmarks, mp_face_mesh.FACEMESH_TESSELATION,
                    mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=0, circle_radius=1))

                # Get eye coordinates
                left_eye = face_landmarks.landmark[LEFT_EYE[0]]
                right_eye = face_landmarks.landmark[RIGHT_EYE[0]]

                # Convert to pixel coordinates
                h, w, _ = frame.shape
                left_eye_x = int(left_eye.x * w)
                right_eye_x = int(right_eye.x * w)
                left_eye_y = int(left_eye.y * h)
                right_eye_y = int(right_eye.y * h)

                # Eye tracking logic
                face_center1 = (left_eye_x + right_eye_x) // 2
                frame_center1 = w // 2
                face_center2 = (left_eye_y + right_eye_y) // 2
                frame_center2 = h // 2
                offset1 = abs(face_center1 - frame_center1)
                offset2 = abs(face_center2 - frame_center2)

                if offset1 > w * 0.035 or offset2 > h * 0.055:  # Threshold for looking away
                    look_away_counter += 1
                else:
                    look_away_counter = 0

                # Suspicious Activity Alert
                if look_away_counter >= LOOK_AWAY_THRESHOLD:
                    alert_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    suspicious_events.append(f"{alert_time}: Suspicious Activity Detected")
                    cv2.putText(frame, 'ALERT: Suspicious Activity Detected!', (30, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        # Update live graph data
        suspicion_levels.append(look_away_counter)
        time_stamps.append(time.time() - start_time)

        plt.draw()
        plt.pause(0.001)

        # Display the output
        cv2.imshow('E-Proctoring System', frame)

        # Exit on 'q'
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

# Generate session report
session_end_time = datetime.datetime.now()
duration = session_end_time - session_start_time
report_filename = f"session_report_{session_end_time.strftime('%Y%m%d_%H%M%S')}.txt"
graph_filename = f"suspicion_graph_{session_end_time.strftime('%Y%m%d_%H%M%S')}.png"

# Save final graph
plt.ioff()
plt.figure()
plt.plot(time_stamps, suspicion_levels, 'r-', label='Suspicion Level')
plt.xlabel('Time (s)')
plt.ylabel('Suspicion Level')
plt.title('Suspicion Level Over Time')
plt.legend()
plt.savefig(graph_filename)
plt.close()

with open(report_filename, 'w') as report_file:
    report_file.write(f"E-Proctoring Session Report\n")
    report_file.write(f"Session Start Time: {session_start_time}\n")
    report_file.write(f"Session End Time: {session_end_time}\n")
    report_file.write(f"Total Duration: {duration}\n")
    report_file.write(f"Total Suspicious Events: {len(suspicious_events)}\n")
    report_file.write(f"Suspicion Graph: {graph_filename}\n")
    report_file.write("\nSuspicious Activity Log:\n")
    for event in suspicious_events:
        report_file.write(event + "\n")

print(f"Session report saved as {report_filename}")
print(f"Suspicion graph saved as {graph_filename}")

# Release resources
cap.release()
cv2.destroyAllWindows()
