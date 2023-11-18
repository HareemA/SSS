import cv2
import pandas as pd
import numpy as np
from ultralytics import YOLO
from tracker import Tracker
from deepface import DeepFace
from flask import Flask, jsonify, Response
from flask_cors import CORS
import base64
from datetime import datetime
from threading import Lock
import face_recognition
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from Group_Gender import *

app = Flask(__name__)
CORS(app)

frame_lock = Lock()

model=YOLO('yolov8n.pt')

gender_model = load_model('gender_detection.model')
classes = ['man', 'woman']

count = detected = enter = exit = male = female = unknown = people = group_count = 0


people_enter={}
counter1=[]

people_exit={}
counter2=[]

frame_to_send = None

cap = cv2.VideoCapture('H:\\Downloads\\26102023_2.mp4')

def processing():
    
    global cap, area1, area2

    while True:    
        ret,frame = cap.read()
        
        if not cap:
            cap = cv2.VideoCapture('H:\\Downloads\\26102023_2.mp4')
            
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
        
        list=[]         
        for index,row in px.iterrows():
            x3=int(row[0])
            y3=int(row[1])
            x4=int(row[2])
            y4=int(row[3])
            d=int(row[5])
            id = int(row[4])
            
        
            x_centre= (x3+x4)//2
            y_centre=(y3+y4)//2

                        
            cv2.rectangle(frame,(x3,y3),(x4,y4),(255,0,0),1)
            
          
        # coordinate_groups = group_coordinates(original_coordinates, group_threshold)

        # #Iterate through the grouped coordinates and draw bounding boxes around groups
        # for group_key, group_coord in coordinate_groups.items():
        #     if len(group_coord) >= 2:
        #         #print("Group detected, key:", group_key)
        #         group_count = group_count + 1
        #         min_x = min([x1 for (x1, y1, x2, y2) in group_coord])
        #         min_y = min([y1 for (x1, y1, x2, y2) in group_coord])
        #         max_x = max([x2 for (x1, y1, x2, y2) in group_coord])
        #         max_y = max([y2 for (x1, y1, x2, y2) in group_coord])
        #         cv2.rectangle(frame, (min_x, min_y), (max_x, max_y), (0, 0, 255), 2)

        with frame_lock:
            frame_to_send = frame
        

@app.route('/get_frame/<int:group_threshold>', methods=['GET'])
def get_data(group_threshold):
    global frame_to_send
    
    with frame_lock:
        if frame_to_send is None:
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


if __name__ == '__main__':
    thread = threading.Thread(target=processing)
    thread.start()
    app.run(host='192.168.100.10', port=8080)

