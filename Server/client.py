import base64
import cv2
import requests
import numpy as np


server_url = 'http://192.168.43.125:8080/get_latest_processed_frame'  # Replace with the correct server URL

while True:
    try:
        response = requests.get(server_url)

        if response.status_code == 200:
            response_data = response.json()

            # Extract the count and frame data from the JSON response
            count = response_data['count']
            grp_count = response_data['Group count']

            frame_bytes = response_data['frame'].encode('utf-8')
            frame_data = base64.b64decode(frame_bytes)
            nparr = np.frombuffer(frame_data, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)


            if frame is not None:
                #cv2.putText(frame, f'Count: {count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(frame, f'Group Count: {grp_count}', (50, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                print("Count:",count)

                cv2.imshow('Latest Processed Frame', frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                print('Error: Unable to decode frame')
        elif response.status_code == 404:
            print('No processed frame available')
        else:
            print('Error:', response.status_code)

    except Exception as e:
        print('Error:', str(e))

cv2.destroyAllWindows()

# import socketio

# # Create a Socket.IO client instance
# sio = socketio.Client()

# @sio.on('connect')
# def on_connect():
#     print('Connected to the server')

# @sio.on('disconnect')
# def on_disconnect():
#     print('Disconnected from the server')

# @sio.on('processed_frame')
# def on_processed_frame(data):
#     print('Received processed frame data:')
#     print(data)
#     # Process the received data as needed (e.g., display the frame, count, groupCount, etc.)

# # Connect to the Socket.IO server
# sio.connect('http://192.168.100.10:8080')

# # Keep the client running
# sio.wait()

