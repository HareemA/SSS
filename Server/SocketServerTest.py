import cv2
import pandas as pd
from ultralytics import YOLO
from tracker import *
import socket
import pickle

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
host = '192.168.126.71'  
port = 8080  # Choose a port to listen on
server_socket.bind((host, port))
server_socket.listen(5)

# Accept client connections
print(f"Waiting for clients to connect on {host}:{port}...")
client_socket, client_address = server_socket.accept()
print(f"Client {client_address} connected!")

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        count += 1
        if count % 3 != 0:
            continue

        conf_thresh = 0.5

        results = model.predict(frame, classes=[0])
        a = results[0].boxes.boxes
        px = pd.DataFrame(a).astype("float")
        obj_list = []
        for index, row in px.iterrows():
            x1 = int(row[0])
            y1 = int(row[1])
            x2 = int(row[2])
            y2 = int(row[3])
            d = int(row[5])
            obj_list.append([x1, y1, x2, y2])

        bbox_idx = tracker.update(obj_list)
        person_count = len(bbox_idx)

        count_message = f"Detected people: {person_count}"

        # Send the count information to the connected client
        client_socket.send(count_message.encode())

        # Serialize and send the current frame to the connected client
        frame_data = pickle.dumps(frame)
        client_socket.send(frame_data)

        for bbox in bbox_idx:
            x3, y3, x4, y4, id = bbox
            cx = int(x3 + x4) // 2
            cy = int(y3 + y4) // 2
            cv2.rectangle(frame, (x3, y3), (x4, y4), (0, 255, 0), 2)
            cv2.putText(frame, str(int(id)), (x3, y3), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0), 1)

        cv2.imshow("RGB", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the client socket, server socket, and OpenCV window
    client_socket.close()
    server_socket.close()
    cv2.destroyAllWindows()
