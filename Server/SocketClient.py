import socket
import pickle
import cv2

# Create a socket client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('192.168.126.71', 8080)  # Replace with the actual IP address of the server

try:
    client_socket.connect(server_address)
    print(f"Connected to {server_address}")
except ConnectionError as e:
    print(f"Connection error: {e}")
    exit()

try:
    while True:
        # Receive count information
        count_data = client_socket.recv(1024)
        if not count_data:
            print("Count data not received. Exiting.")
            break

        count_message = count_data.decode()
        count = int(count_message.split(":")[1])

        # Receive and deserialize the frame
        frame_data = b""
        while len(frame_data) < 10000:
            chunk = client_socket.recv(10000 - len(frame_data))
            if not chunk:
                print("Frame data not received completely. Exiting.")
                break
            frame_data += chunk

        if len(frame_data) == 10000:
            frame = pickle.loads(frame_data)

            # Display the received frame and count
            cv2.imshow("Received Frame", frame)
            print(count_message)
            print("Person Count:", count)

            if cv2.waitKey(1) & 0xFF == 27:
                break
        else:
            print("Frame data not received completely. Exiting.")
            break
except Exception as e:
    print(f"An error occurred: {e}")

# Close the client socket and OpenCV window
client_socket.close()
cv2.destroyAllWindows()
