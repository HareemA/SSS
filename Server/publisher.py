import cv2
import requests
import numpy as np

video_path = './store.mp4'
cap = cv2.VideoCapture(video_path)

server_url = 'http://192.168.203.125:8080/update_frame'  # Use the correct URL for the update_frame route

while True:
    ret, frame = cap.read()
    if not ret:
        break

    _, buffer = cv2.imencode('.jpg', frame)
    frame_bytes = buffer.tobytes()

    # Send the frame data in the request body as bytes
    response = requests.post(server_url, data=frame_bytes, headers={'Content-Type': 'application/octet-stream'})

# Release the video capture
cap.release()
