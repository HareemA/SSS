import cv2
import requests
import base64
from pytube import YouTube
import pafy

import pafy
import cv2

url = "https://www.youtube.com/live/gFRtAAmiFbE?si=5_EYmYmb6QeiomQB"
video = pafy.new(url)
best = video.getbest(preftype="mp4")

server_url = 'http://192.168.100.10:8080/update_frame'

cap = cv2.VideoCapture(best.url)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to JPEG format
    _, buffer = cv2.imencode('.jpg', frame)
    frame_bytes = buffer.tobytes()

    # Encode the frame in base64
    frame_base64 = base64.b64encode(frame_bytes).decode('utf-8')

    # Send the frame to your server
    response = requests.post(server_url, json={'frame': frame_base64})

    # Optionally, you can print the server response or handle it as needed
    print("Server Response:", response.text)

# Release the video capture
cap.release()
