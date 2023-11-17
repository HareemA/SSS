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

app = Flask(__name__)
CORS(app)

frame_lock = Lock()

model=YOLO('yolov8n.pt')

gender_model = load_model('gender_detection.model')
classes = ['man', 'woman']

count = detected = enter = exit = male = female = unknown = people = group_count = 0

area1=[(135,186),(811,307),(802,342),(103,203)]
area2=[(176,159),(818,263),(812,301),(135,186)]

people_enter={}
counter1=[]

people_exit={}
counter2=[]

frame_to_send = None

cap = cv2.VideoCapture('E:\\Freelance Projects\\Shop Surveillance System\\video\\vid.mp4')

def processing():
    
    global cap, count, group_count, detected, area1, area2, people_enter, people_exit, counter1
    global counter2, enter, exit, male, female, unknown, people, frame_to_send, frame_lock

    while True:    
        ret,frame = cap.read()
        
        if not cap:
            cap = cv2.VideoCapture('E:\\Freelance Projects\\Shop Surveillance System\\video\\vid.mp4')
            
        if not ret:
            cap.release()
            cap = None
            continue
        
        count += 1
        if count % 3 != 0:
            continue
        
        frame=cv2.resize(frame,(1020,500))
        
        original_coordinates = []  
        group_threshold = 35
        
        #Dfining areas for detection
        cv2.polylines(frame,[np.array(area1,np.int32)],True,(0,0,255),1)
        cv2.polylines(frame,[np.array(area2,np.int32)],True,(0,255,0),1)   

        results=model.track(frame, conf = 0.3,classes=[0],persist=True)
        a=results[0].boxes.data
        px=pd.DataFrame(a).astype("float")
        
        gender_label = 'none'

        list=[]         
        for index,row in px.iterrows():
            x3=int(row[0])
            y3=int(row[1])
            x4=int(row[2])
            y4=int(row[3])
            d=int(row[5])
            id = int(row[4])
            
            #For group detection
            original_coordinates.append([x3, y3, x4, y4])
    
            x_centre= (x3+x4)//2
            y_centre=(y3+y4)//2

            person=frame[y3:y4,x3:x4]
            face_crop = cv2.resize(person, (96, 96))
            face_crop = face_crop.astype("float") / 255.0
            face_crop = img_to_array(face_crop)
            face_crop = np.expand_dims(face_crop, axis=0)

            gender_confidence = gender_model.predict(face_crop)[0]
            gender_index = np.argmax(gender_confidence)
            gender_label = classes[gender_index]

            #people leave
            #result is 1 if rerson inside that area and -1 if person isnt inside the area
            #x _centre,y4
            results1 = cv2.pointPolygonTest(np.array(area1,np.int32),((x_centre,y_centre)),False)
            if results1>=0:
                people_exit[id]=(x4,y4)
            if id in people_exit:
                results2 = cv2.pointPolygonTest(np.array(area2,np.int32),((x_centre,y_centre)),False)
                if results2>=0:
                    if counter2.count(id)==0:
                        counter2.append(id)
                        exit=exit+1
     
            #People Enter
            results3 = cv2.pointPolygonTest(np.array(area2,np.int32),((x_centre,y_centre)),False)
            if results3>=0:
                #print("result3:",results3)
                people_enter[id]=(x4,y4)
            if id in people_enter:
                results4 = cv2.pointPolygonTest(np.array(area1,np.int32),((x_centre,y_centre)),False)
                if results4>=0:
                    if counter1.count(id)==0:
                        counter1.append(id)
                        enter=enter+1
                        if gender_label == 'man':
                            male = male + 1
                        elif gender_label == 'woman':
                            female = female + 1
                        else:
                            unknown = unknown + 1
     
            if(enter>exit):      
                detected = enter - exit
                        
            cv2.rectangle(frame,(x3,y3),(x4,y4),(255,0,0),1)
            cv2.circle(frame,(x_centre,y_centre),4,(255,0,0),-1)
            cv2.putText(frame,str(int(id)),(x3,y3),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,0,0),1)
            cv2.putText(frame,gender_label,((x3+19),y3),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,0,0),1)
          
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
        

@app.route('/get_data/<int:group_threshold>', methods=['GET'])
def get_data(group_threshold):
    global frame_to_send, detected, group_count, enter, exit, male, female, unknown, frame_lock
    print("In server")
    print("Enter count: ",enter)
    print("Exit count:", exit)
    print("Men: ",male)
    print("Women: ",female)
    print("InStore: ", detected)
    
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
            'inStore': detected,
            'group_count': group_count,
            'enter': enter,
            'exit': exit,
            'male': male,
            'female': female,
            'unknown': unknown,
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
    thread = threading.Thread(target=processing)
    thread.start()
    app.run(host='192.168.18.132', port=8080)

