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
from fpdf import FPDF

# Setup folders
if not os.path.exists("reports"):
    os.makedirs("reports")

# Initialize MediaPipe
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

LEFT_EYE = [33, 133]
RIGHT_EYE = [362, 263]
LOOK_AWAY_THRESHOLD = 3

cap = cv2.VideoCapture(0)

look_away_counter = 0
suspicious_events = []
session_start_time = datetime.datetime.now()

suspicion_levels = deque(maxlen=100)
time_stamps = deque(maxlen=100)
start_time = time.time()

# Live plot
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

with mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True,
                           min_detection_confidence=0.5,
                           min_tracking_confidence=0.5) as face_mesh:
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

                face_center1 = (left_eye_x + right_eye_x) // 2
                frame_center1 = w // 2
                face_center2 = (left_eye_y + right_eye_y) // 2
                frame_center2 = h // 2
                offset1 = abs(face_center1 - frame_center1)
                offset2 = abs(face_center2 - frame_center2)

                if offset1 > w * 0.055 or offset2 > h * 0.075:
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

# Finalize session
session_end_time = datetime.datetime.now()
duration = session_end_time - session_start_time

timestamp = session_end_time.strftime('%Y%m%d_%H%M%S')
graph_filename = f"suspicion_graph_{timestamp}.png"
final_pdf_filename = f"session_report_{timestamp}.pdf"

# Save Graph
plt.ioff()
plt.figure()
plt.plot(time_stamps, suspicion_levels, 'r-', label='Suspicion Level')
plt.xlabel('Time (s)')
plt.ylabel('Suspicion Level')
plt.title('Suspicion Level Over Time')
plt.legend()
plt.savefig(f"reports/{graph_filename}")
plt.close()

# Generate PDF Report
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", 'B', 16)
pdf.cell(200, 10, txt="E-Proctoring Session Report", ln=True, align='C')
pdf.ln(10)

pdf.set_font("Arial", size=12)
pdf.cell(200, 10, txt=f"Start Time: {session_start_time}", ln=True)
pdf.cell(200, 10, txt=f"End Time: {session_end_time}", ln=True)
pdf.cell(200, 10, txt=f"Duration: {duration}", ln=True)
pdf.cell(200, 10, txt=f"Suspicious Events: {len(suspicious_events)}", ln=True)
pdf.ln(10)

# Classify suspicion level
total_events = len(suspicious_events)
if total_events <= 100:
    level = "Extremely Low Suspicion"
elif 100 < total_events <= 300:
    level = "Medium Suspicion"
elif 300 < total_events <= 500:
    level = "High Suspicion"
else:
    level = "Very High Suspicion"

pdf.cell(200, 10, txt=f"Suspicion Level: {level}", ln=True)

pdf.ln(10)
pdf.set_font("Arial", 'B', 14)
pdf.cell(0, 10, txt="Suspicion Graph:", ln=True)
pdf.image(f"reports/{graph_filename}", x=10, y=pdf.get_y() + 5, w=180)

pdf.output(f"reports/{final_pdf_filename}")

# Upload to backend
try:
    res = requests.post("http://localhost:5000/save_report", json={
        "report_name": final_pdf_filename,
        "graph_name": graph_filename
    })
    print("✅ Report uploaded:", res.json())
except Exception as e:
    print("❌ Failed to upload report:", e)

cap.release()
cv2.destroyAllWindows()
