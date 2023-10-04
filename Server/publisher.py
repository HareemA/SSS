import cv2
import requests
import numpy as np

video_path = './vidp.mp4'

cap = cv2.VideoCapture('rtsp://admin:Ncsael@123@172.23.16.150:554')

server_url = 'http://172.23.17.3:8080/update_frame'  # Use the correct URL for the update_frame route

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

#############################

# import cv2

# # RTSP URL of the camera stream
# rtsp_url = 'rtsp://admin:Ncsael@123@172.23.16.150:554'

# # Open a connection to the RTSP stream
# cap = cv2.VideoCapture(rtsp_url)

# if not cap.isOpened():
#     print("Error: Could not open RTSP stream.")
#     exit()

# while True:
#     ret, frame = cap.read()
    
#     if not ret:
#         print("Error: Could not read frame.")
#         break

#     # You can process or display the 'frame' here as needed
#     cv2.imshow('RTSP Stream', frame)

#     # Press 'q' to exit the loop
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Release the video capture and close any open windows
# cap.release()
# cv2.destroyAllWindows()
