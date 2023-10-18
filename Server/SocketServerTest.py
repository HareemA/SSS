import cv2
import pandas as pd
import numpy as np
from ultralytics import YOLO
from tracker import *
import socket
import time
import threading

model = YOLO('yolov8s.pt')

def RGB(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        colorsBGR = [x, y]
        print(colorsBGR)

cv2.namedWindow('RGB')
cv2.setMouseCallback('RGB', RGB)

cap = cv2.VideoCapture('E:\\Freelance Projects\\Shop Surveillance System\\video\\rtsp___172.23.16.150_554 - VLC media player 2023-10-16 12-56-14.mp4')

my_file = open("coco.txt", "r")
data = my_file.read()
class_list = data.split("\n")

count = 999
tracker = Tracker()

# Create a socket server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '192.168.143.71'  # Use '0.0.0.0' to bind to all available network interfaces
port = 8080  # Choose a port to listen on
server_socket.bind((host, port))
server_socket.listen(5)

# Accept client connections
print(f"Waiting for clients to connect on {host}:{port}...")
client_socket, client_address = server_socket.accept()
print(f"Client {client_address} connected!")

# Create a thread for sending video frames and count information
def send_video_and_count():
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            count += 1
            if count % 3 != 0:
                continue

            if not frame.any():
                continue

            frame = cv2.resize(frame, (1020, 500))

            # Process the frame and send it
            conf_thresh = 0.5
            results = model.predict(frame, classes=[0])
            a = results[0].boxes.boxes
            px = pd.DataFrame(a).astype("float")
            list = []
            for index, row in px.iterrows():
                x1 = int(row[0])
                y1 = int(row[1])
                x2 = int(row[2])
                y2 = int(row[3])
                d = int(row[5])
                list.append([x1, y1, x2, y2])

            bbox_idx = tracker.update(list)
            count_message = f"Detected people: {len(bbox_idx)}"

            # Send video frame to the client
            frame_bytes = cv2.imencode('.jpg', frame)[1].tobytes()
            client_socket.send(b'FRAME_START')
            client_socket.send(frame_bytes)
            client_socket.send(b'FRAME_END')
            print("Sent a video frame.")

            # Send count information to the client
            client_socket.send(count_message.encode())
            print("Sent count information.")

    except Exception as e:
        print(f"Error in sending video and count information: {e}")

# Start the thread for sending video frames and count information
video_and_count_thread = threading.Thread(target=send_video_and_count)

# Start the thread
video_and_count_thread.start()

# Wait for the thread to finish
video_and_count_thread.join()

# Close the client socket and server socket
client_socket.close()
server_socket.close()
cv2.destroyAllWindows()
