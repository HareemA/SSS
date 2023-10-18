import cv2
import socket
import numpy as np
import threading

# Server information
server_host = '192.168.143.71'  # Change to the server's IP address if needed
server_port = 8080  # Use the same port as the server

# Create a socket for the client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Create an OpenCV window for video display
cv2.namedWindow('Server Video Stream', cv2.WINDOW_NORMAL)

# Create a thread for video frame reception and display
def receive_and_display_video():
    try:
        while True:
            # Receive video frame data from the server
            frame_data = b''
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                frame_data += data
                if b'FRAME_END' in data:
                    break

            # Check for the end of video stream
            if b'VIDEO_END' in frame_data:
                break

            print("Received a video frame.")

            # Decode the received frame and display it using OpenCV
            frame_bytes = frame_data.split(b'FRAME_END')[0]
            frame_np = np.frombuffer(frame_bytes, dtype=np.uint8)
            frame = cv2.imdecode(frame_np, cv2.IMREAD_COLOR)
            cv2.imshow('Server Video Stream', frame)

            # Press 'q' to quit the video display
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except Exception as e:
        print(f"Error in video thread: {e}")

# Create a thread for count information reception and display
def receive_and_display_count():
    try:
        while True:
            # Receive the count information from the server
            count_message = client_socket.recv(1024).decode()
            if not count_message:
                break

            # Print the received count information
            print(f"Received count: {count_message}")

    except Exception as e:
        print(f"Error in count thread: {e}")

# Start the video and count threads
video_thread = threading.Thread(target=receive_and_display_video)
count_thread = threading.Thread(target=receive_and_display_count)

# Connect to the server
client_socket.connect((server_host, server_port))
print(f"Connected to the server at {server_host}:{server_port}")

# Start the threads
video_thread.start()
count_thread.start()

# Wait for the threads to finish
video_thread.join()
count_thread.join()

# Close the client socket
client_socket.close()
cv2.destroyAllWindows()
print("Connection closed.")


