import cv2
cap = cv2.VideoCapture(0)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH),
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT),

iwidth = int(len(width)),
iheight = int(len(height)),

print(f"{iwidth} x {iheight}")

