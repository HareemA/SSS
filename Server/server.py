import cv2
import pandas as pd
import numpy as np
from ultralytics import YOLO
from tracker import *
from flask import Flask, jsonify, render_template, request, Response
import threading 
from flask_cors import CORS 
import base64
from datetime import datetime
from group_test_server import *

app = Flask(__name__)
CORS(app) 


model=YOLO('yolov8s.pt')


my_file = open("coco.txt", "r")
data = my_file.read()
class_list = data.split("\n")
#print(class_list)
count=0
tracker=Tracker()   


latest_frame = None  # Initialize a variable to store the latest frame
detected_persons_count = 0
groupCount = 0

@app.route('/update_frame', methods=['POST'])
def update_frame():
    global latest_frame,detected_persons_count

    try:
        frame_bytes = request.data

        if not frame_bytes:
            return Response('Error: Empty frame data', status=400)

        # Convert frame_bytes to a NumPy array
        frame_array = np.frombuffer(frame_bytes, np.uint8)

        # Decode the frame
        frame = cv2.imdecode(frame_array, cv2.IMREAD_COLOR)

        if frame is None:
            return Response('Error: Unable to decode frame', status=400)

        # Store the latest frame
        latest_frame = frame

        return Response('Frame received', status=200)
    except Exception as e:
        return Response(f'Error: {str(e)}', status=500)



@app.route('/get_latest_processed_frame', methods=['GET'])
def get_latest_processed_frame():
    global latest_frame
    global detected_persons_count
    global groupCount
    try:
        if latest_frame is None :
            return Response('No processed frame available', status=404)
        

        frame , detected_persons_count , groupCount  = main(latest_frame)

        # Convert the processed frame to JPEG format
        #_, encoded_frame = cv2.imencode('.jpg', latest_frame)
        _, encoded_frame = cv2.imencode('.jpg', frame)

        if encoded_frame is None:
            print("Error here")
            return Response('Error: Unable to encode frame', status=500)

        frame_bytes = base64.b64encode(encoded_frame)
        timestamp = datetime.now().strftime('%H:%M:%S')
        
        #be sure to decode frame on clients side
        response_data = {
            'count': detected_persons_count,
            'frame': frame_bytes.decode('utf-8'),  # Convert bytes to a string
            'Group count': groupCount,
            'time' : timestamp
        }
        return jsonify(response_data)

       
    except Exception as e:
        print(e)
        return Response(f'Error: {str(e)}', status=500)



if __name__ == '__main__':
    app.run(host='192.168.18.132',port=8080)

    
