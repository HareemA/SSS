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


# video_link = '"E:\\Freelance Projects\\Shop Surveillance System\\video\\vid.mp4"'
video_link= "H:\\Downloads\\26102023_4.mp4"
# video_link = 'E:\\Freelance Projects\\Shop Surveillance System\\video\\vid.mp4'
cap = cv2.VideoCapture(video_link)

model=YOLO('yolov8n.pt')

frame_lock = threading.Lock()

frame_update=None

count=0

# area1=[(1,367),(800,357),(792,406),(1,403)]
area1=[(2,322),(807,317),(801,355),(4,360)]

def frame_to_send():

    global count, frame_update, group_lock, group_threshold, cap, video_link
    
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
                min_x = min([x1 for (x1, y1, x2, y2) in group_coord])
                min_y = min([y1 for (x1, y1, x2, y2) in group_coord])
                max_x = max([x2 for (x1, y1, x2, y2) in group_coord])
                max_y = max([y2 for (x1, y1, x2, y2) in group_coord])
                cv2.rectangle(frame, (min_x, min_y), (max_x, max_y), (0, 0, 255), 2)

        with frame_lock:
            frame_update = frame
        

@app.route('/get_frame/<int:group_thresh>', methods=['GET'])
def get_frame(group_thresh):
    global frame_update, group_lock, group_threshold, frame_lock
    
    with group_lock:
        group_threshold = group_thresh
    
    with frame_lock:
        if frame_to_send is None:
            print("No frame found")
            return Response('Error: No frame available', status=500)

        _, encoded_frame = cv2.imencode('.jpg', frame_update)

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
    
#API for Pie for gender distribution Daily    
@app.route('/get_gender_pie_data', methods=['GET'])
def get_gender_pie_data():
    print("in pie data 1")
    data = get_daily_gender_distribution()  

    # print(data)
    return jsonify(data)


#API for Line CHart Daily
@app.route('/daily_line_chart', methods=['GET'])
def daily_line_chart():
    data = get_daily_line_data()
    # print(data)

    return jsonify(data)

#API for Line CHart Weekly
@app.route('/weekly_line_chart', methods=['GET'])
def weekly_line_chart():
    data = get_weekly_line_data()
    # print(data)

    return jsonify(data)

#API for Line CHart Monthly
@app.route('/monthly_line_chart', methods=['GET'])
def monthly_line_chart():
    data = get_monthly_line_data()
    # print(data)

    return jsonify(data)

@app.route('/get_card_data',methods=['GET'])
def get_card_data():
    data=chart_data()
    return jsonify(data)

    
#API for Repeat Ratio Pie
@app.route('/repeat_ratio_pie', methods=['GET'])
def repeat_ratio_pie():
    data = get_repeat_ratio_pie_data()
    # print(data)

    return jsonify(data)

#API for Group Ratio Pie
@app.route('/group_ratio_pie', methods=['GET'])
def group_ratio_pie():
    data = get_group_pie_data()
    # print(data)

    return jsonify(data)

#API for Bar Daily Gender Distribution
@app.route('/daily_gender_bar', methods=['GET'])
def daily_gender_bar():
    data = get_daily_gender_bar_data()
    # print(data)

    return jsonify(data)

#API for Bar Engagement Graph
@app.route('/daily_engagement_bar', methods=['GET'])
def daily_engagement_bar():
    data = get_engagement_bar_data()
    # print(data)

    return jsonify(data)


#API for Customers Table
@app.route('/customers_table', methods=['GET'])
def customers_table():
    data = get_customers_table_data()
    # print(data)

    return jsonify(data)

  

if __name__ == '__main__':
    frame_thread = threading.Thread(target=frame_to_send)
    processing_thread = threading.Thread(target=processing)
    

    frame_thread.start()
    processing_thread.start()
    

    app.run(host='192.168.100.10', port=8080)
    

