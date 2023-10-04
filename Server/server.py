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
from pytube import YouTube
import threading


app = Flask(__name__)
CORS(app) 

lock = threading.Lock()

lock = threading.Lock()


latest_frame = None  # Initialize a variable to store the latest frame
detected_persons_count = 0
groupCount = 0
latest_gender_frame = None
female_count = 0
male_count=0

video_path = './vidp.mp4'
cap = cv2.VideoCapture(video_path)
#"rtsp://admin:PNcsael@123@172.23.16.150:554"


def capture_frames():
    global latest_frame
    global cap

    while True:
        if not cap:
            cap = cv2.VideoCapture(video_path)

        ret, frame = cap.read()
        if not ret:
            print("Error reading frame. Reopening the stream...")
            cap.release()
            cap = None
            continue

        try:
            latest_frame = frame
        except cv2.error as e:
            print("Hadia shafqat")
            print(f"Error while decoding frame: {e}")
            continue  # Skip the problematic frame
video_path = './vidp.mp4'
cap = cv2.VideoCapture('rtsp://admin:Ncsael-123@172.23.16.150:554')
#"rtsp://admin:PNcsael@123@172.23.16.150:554"


def capture_frames():
    global latest_frame
    global cap

    while True:
        if not cap:
            cap = cv2.VideoCapture('rtsp://admin:Ncsael-123@172.23.16.150:554')

        ret, frame = cap.read()
        if not ret:
            print("Error reading frame. Reopening the stream...")
            cap.release()
            cap = None
            continue

        try:
            latest_frame = frame
        except cv2.error as e:
            print("Hadia shafqat")
            print(f"Error while decoding frame: {e}")
            continue  # Skip the problematic frame

        if cv2.waitKey(1) & 0xFF == 27: 
            break

    #if cap:
    cap.release()
    cv2.destroyAllWindows()


@app.route('/get_latest_processed_frame/<int:group_threshold>', methods=['GET'])
def get_latest_processed_frame(group_threshold):
    global latest_frame
    global detected_persons_count
    global groupCount
    try:
        if latest_frame is None :
            return Response('No processed frame available', status=404)
        
        
        frame , detected_persons_count , groupCount  = main(latest_frame,group_threshold)

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
            'groupCount': groupCount,
            'time' : timestamp
        }
        return jsonify(response_data)

       
    except Exception as e:
        print(e)
        return Response(f'Error: {str(e)}', status=500)



# @app.route('/get_gender_count', methods=['GET'])
# def get_gender_count():
#     global male_count
#     global female_count

#     response_data = {
#         'male_count': male_count,
#         'female_count': female_count
#     }
    
#     return jsonify(response_data)



if __name__ == '__main__':
    thread = threading.Thread(target=capture_frames)
    thread.start()
    app.run(host='172.23.17.3',port=8080)

    
