import cv2
import numpy as np
from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import base64
from datetime import datetime
from group_test_server import *

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")  # Allow connections from any origin for this example

latest_frame = None
detected_persons_count = 0
groupCount = 0

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


@app.route('/update_frame', methods=['POST'])
def update_frame():
    global latest_frame
    print("Update frame working")

    try:
        frame_bytes = request.data

        if not frame_bytes:
            return Response('Error: Empty frame data', status=400)

        # Convert frame_bytes to a NumPy array
        frame_array = np.frombuffer(frame_bytes, np.uint8)

        # Decode the frame
        frame = cv2.imdecode(frame_array, cv2.IMREAD_COLOR)

        if frame is not None:
            # Store the latest frame from the React client
            latest_frame = frame

        return Response('Frame received', status=200)
    except Exception as e:
        return Response(f'Error: {str(e)}', status=500)


@socketio.on('get_latest_processed_frame')
def get_latest_processed_frame():
    global latest_frame, detected_persons_count, groupCount

    try:
        if latest_frame is None:
            return

        frame, detected_persons_count, groupCount = main(latest_frame)

        # Convert the processed frame to JPEG format
        _, encoded_frame = cv2.imencode('.jpg', frame)

        if encoded_frame is not None:
            frame_bytes = base64.b64encode(encoded_frame).decode('utf-8')
            timestamp = datetime.now().strftime('%H:%M:%S')

            response_data = {
                'count': detected_persons_count,
                'frame': frame_bytes,
                'Group count': groupCount,
                'time': timestamp
            }

            # Send the processed frame and data to the client
            socketio.emit('processed_frame', response_data, broadcast=True)
    except Exception as e:
        print(f'Error: {str(e)}')


if __name__ == '__main__':
    socketio.run(app, host='192.168.100.10', port=8080)
