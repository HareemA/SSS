import cv2
import pandas as pd
import numpy as np
from ultralytics import YOLO
from tracker import Tracker
from deepface import DeepFace
from flask import Flask, jsonify, Response
from flask_cors import CORS
import base64
from database import *
from datetime import datetime
from threading import Lock
import face_recognition
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from Group_Gender import *
from GroupDetection import *

app = Flask(__name__)
CORS(app)


video_link = 'H:\\Downloads\\26102023_2.mp4'
cap = cv2.VideoCapture(video_link)

model=YOLO('yolov8n.pt')

frame_lock = threading.Lock()

frame_to_send=None

count=0

area1=[(1,367),(800,357),(792,406),(1,403)]
area2=[(2,322),(807,317),(801,355),(4,360)]

def frame_to_send():
    
    global cap, area1, area2, group_lock, group_threshold,count, frame_to_send

    while True:    
        ret,frame = cap.read()
        
        if not cap:
            cap = cv2.VideoCapture(video_link)
            
        if not ret:
            cap.release()
            cap = None
            continue
        
        count += 1
        if count % 3 != 0:
            continue
        
        frame=cv2.resize(frame,(1020,500))
        
        #Dfining areas for detection
        cv2.polylines(frame,[np.array(area1,np.int32)],True,(0,0,255),1)
        cv2.polylines(frame,[np.array(area2,np.int32)],True,(0,255,0),1)   

        results=model.track(frame, conf = 0.3,classes=[0],persist=True)
        a=results[0].boxes.data
        px=pd.DataFrame(a).astype("float")
        
        original_coordinates = []  
        
        list=[]         
        for index,row in px.iterrows():
            x3=int(row[0])
            y3=int(row[1])
            x4=int(row[2])
            y4=int(row[3])
            d=int(row[5])
            id = int(row[4])
            
            original_coordinates.append([x3, y3, x4, y4])

                        
            cv2.rectangle(frame,(x3,y3),(x4,y4),(255,0,0),1)
            
        with group_lock:
            coordinate_groups = group_coordinates(original_coordinates, group_threshold)

        #Iterate through the grouped coordinates and draw bounding boxes around groups
        for group_key, group_coord in coordinate_groups.items():
            if len(group_coord) >= 2:
                #print("Group detected, key:", group_key)
                group_count = group_count + 1
                min_x = min([x1 for (x1, y1, x2, y2) in group_coord])
                min_y = min([y1 for (x1, y1, x2, y2) in group_coord])
                max_x = max([x2 for (x1, y1, x2, y2) in group_coord])
                max_y = max([y2 for (x1, y1, x2, y2) in group_coord])
                cv2.rectangle(frame, (min_x, min_y), (max_x, max_y), (0, 0, 255), 2)

        with frame_lock:
            frame_to_send = frame
        

@app.route('/get_frame/<int:group_thresh>', methods=['GET'])
def get_data(group_thresh):
    global frame_to_send, group_lock, group_threshold
    
    with group_lock:
        group_threshold = group_thresh
    
    with frame_lock:
        if frame_to_send is None:
            print("No frame found")
            return Response('Error: No frame available', status=500)

        _, encoded_frame = cv2.imencode('.jpg', frame_to_send)

        if encoded_frame is None:
            print("Error here")
            return Response('Error: Unable to encode frame', status=500)

        frame_bytes = base64.b64encode(encoded_frame)
        timestamp = datetime.now().strftime('%H:%M:%S')
        response_data = {
            'frame': frame_bytes.decode('utf-8'),
            'time': timestamp
        }

        return jsonify(response_data)
    


    
@app.route('/get_gender_pie_data', methods=['GET'])
def get_gender_pie_data():
    print("in pie data 1")
    data = get_daily_gender_distribution()  # Use the function from the previous response

    gender_pie_data = [
        {
            'id': 'Man',
            'label': 'Man',
            'value': data['male_percentage'],  # Replace with the actual percentage for men
            'color': 'hsl(104, 70%, 50%)',
        },
        {
            'id': 'Woman',
            'label': 'Woman',
            'value': data['female_percentage'],  # Replace with the actual percentage for women
            'color': 'hsl(162, 70%, 50%)',
        },
        {
            'id': 'Unidentified',
            'label': 'Unidentified',
            'value': data['unknown_percentage'],  # Replace with the actual percentage for unidentified
            'color': 'hsl(291, 70%, 50%)',
        },
    ]

    print(gender_pie_data)
    return jsonify(gender_pie_data)


#API for Line CHart
@app.route('/daily_line_chart', methods=['GET'])
def daily_line_chart():
    data = get_daily_line_data()

    # # Format the data as per the provided structure
    # lineChartDataDaily = [
    #     {
    #         'id': 'ENTERED',
    #         'color': 'tokens("dark").redAccent[600]',
    #         'data': [{'x': interval, 'y': data[interval]['Enter']} for interval in data]
    #     },
    #     {
    #         'id': 'LEFT',
    #         'color': 'tokens("dark").blueAccent[400]',
    #         'data': [{'x': interval, 'y': data[interval]['Exit']} for interval in data]
    #     },
    #     {
    #         'id': 'MIN',
    #         'color': 'tokens("dark").greenAccent[600]',
    #         'data': [{'x': interval, 'y': data[interval]['Min']} for interval in data]
    #     },
    #     {
    #         'id': 'MAX',
    #         'color': 'tokens("dark").redAccent[300]',
    #         'data': [{'x': interval, 'y': data[interval]['Max']} for interval in data]
    #     },
    # ]

    print(data)

    return jsonify(data)

  
if __name__ == '__main__':
    processing_thread = threading.Thread(target=processing)
    frame_thread = threading.Thread(target=frame_to_send)

    frame_thread.start()
    processing_thread.start()
    

    app.run(host='192.168.100.10', port=8080)
    

