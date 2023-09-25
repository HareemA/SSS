import requests
import cv2
from pytube import YouTube
#try using pafy for live

# YouTube video URL
youtube_url = 'https://youtu.be/KMJS66jBtVQ?si=oqq7Sp4iQ4M1TFSQ'
#https://youtu.be/KMJS66jBtVQ?si=oqq7Sp4iQ4M1TFSQ
#https://youtu.be/-8iq5uHKvfU?si=yFiIvsM0IpbinZtp
#ttps://www.youtube.com/live/DjdUEyjx8GM?si=icPQiRxVB2afYEoA
# Create a YouTube object
yt = YouTube(youtube_url)

# Get the stream with the highest resolution
stream = yt.streams.get_highest_resolution()

# OpenCV VideoCapture from the stream URL
cap = cv2.VideoCapture(stream.url)

server_url = 'http://192.168.100.10:8080/update_frame'  # Use the correct URL for the update_frame route

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
