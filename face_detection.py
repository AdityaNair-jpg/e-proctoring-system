import cv2
import mediapipe as mp

# Initialize MediaPipe Face Detection
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

# OpenCV Video Capture
cap = cv2.VideoCapture(0)  # 0 is the default webcam

# Face Detection Model
with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5) as face_detection:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            break

        # Convert the frame to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame with MediaPipe
        results = face_detection.process(rgb_frame)

        # Draw face detections
        if results.detections:
            for detection in results.detections:
                mp_drawing.draw_detection(frame, detection)

        # Display the output
        cv2.imshow('E-Proctoring Face Detection', frame)

        # Break the loop on 'q' key press
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

# Release resources
cap.release()
cv2.destroyAllWindows()
