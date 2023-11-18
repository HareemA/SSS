import cv2
import pandas as pd
import numpy as np
from ultralytics import YOLO
from tracker import*
from deepface import DeepFace
import os
import face_recognition
import threading
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from database import *


model=YOLO('yolov8n.pt')

gender_model = load_model('gender_detection.model')
classes = ['man', 'woman']
# def RGB(event, x, y, flags, param):
#     if event == cv2.EVENT_MOUSEMOVE :  
#         colorsBGR = [x, y]
#         print(colorsBGR)
        
# cv2.namedWindow('RGB')
# cv2.setMouseCallback('RGB', RGB)

count = detected = enter = exit = male = female = unknown = people = group_count = 0

area1=[(1,367),(800,357),(792,406),(1,403)]
area2=[(2,322),(807,317),(801,355),(4,360)]

people_enter={}
counter1=[]

people_exit={}
counter2=[]

frame_to_send = None

group_val = False

group_threshold = 55

group_lock = threading.Lock()

video_link = 'H:\\Downloads\\26102023_2.mp4'

cap = cv2.VideoCapture(video_link)

def processing():
    
    global cap, count, group_count, detected, area1, area2, people_enter, people_exit, counter1, group_val
    global counter2, enter, exit, male, female, unknown, people, frame_to_send, group_threshold, video_link
    

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
        
        original_coordinates = []  
        
        group_stat={}
        
        #Dfining areas for detection
        cv2.polylines(frame,[np.array(area1,np.int32)],True,(0,0,255),1)
        cv2.polylines(frame,[np.array(area2,np.int32)],True,(0,255,0),1)   

        results=model.track(frame, conf = 0.3,classes=[0],persist=True)
        a=results[0].boxes.data
        px=pd.DataFrame(a).astype("float")
        
        gender_label = 'none'

        list=[]         
        
        #Iterate through all the  points to group them
        for index,row in px.iterrows():
            x3=int(row[0])
            y3=int(row[1])
            x4=int(row[2])
            y4=int(row[3])
            d=int(row[5])
            id = int(row[4])
            
            #For group detection
            original_coordinates.append({'id': id, 'coord': [x3, y3, x4, y4]})
            
        with group_lock:
            coordinate_groups = group_coordinates(original_coordinates, group_threshold)
            
        group_stat=process_groups(coordinate_groups)
        print("Group_stat: ",group_stat)

        #Now iterate through all the points again to predict gender, perform facial rec and add in database etc.
        for index,row in px.iterrows():
            x3=int(row[0])
            y3=int(row[1])
            x4=int(row[2])
            y4=int(row[3])
            d=int(row[5])
            id = int(row[4])
            
            x_centre= (x3+x4)//2
            y_centre=(y3+y4)//2

            person=frame[y3:y4,x3:x4]
            
            group_val = group_stat[id]
            
            face_crop = cv2.resize(person, (96, 96))
            face_crop = face_crop.astype("float") / 255.0
            face_crop = img_to_array(face_crop)
            face_crop = np.expand_dims(face_crop, axis=0)

            gender_confidence = gender_model.predict(face_crop)[0]
            gender_index = np.argmax(gender_confidence)
            gender_label = classes[gender_index]

            #people leave
            results1 = cv2.pointPolygonTest(np.array(area1,np.int32),((x_centre,y_centre)),False)
            if results1>=0:
                people_exit[id]=(x4,y4)
                
            if id in people_exit:
                results2 = cv2.pointPolygonTest(np.array(area2,np.int32),((x_centre,y_centre)),False)
                if results2>=0:
                    # if counter2.count(id)==0:
                    encodings = encode_face_image(person)
                    # counter2.append(id)
                    exit=exit+1
                    #SENDING DATA TO DATABASE TO BE STORED    
                    customer_leaving(encodings)
     
            #People Enter
            results3 = cv2.pointPolygonTest(np.array(area2,np.int32),((x_centre,y_centre)),False)
            if results3>=0:
                #print("result3:",results3)
                people_enter[id]=(x4,y4)
                
            if id in people_enter:
                results4 = cv2.pointPolygonTest(np.array(area1,np.int32),((x_centre,y_centre)),False)
                if results4>=0:
                    #if counter1.count(id)==0:
                    encodings = encode_face_image(person)
                    
                    # counter1.append(id)
                    enter=enter+1
                    if gender_label == 'man':
                        gender="Male"
                        male = male + 1
                    elif gender_label == 'woman':
                        gender="Female"
                        female = female + 1
                    else:
                        unknown = unknown + 1
                        gender="Unknown"
                    #SENDING DATA TO DATABASE TO BE STORED    
                    customer_exist(encodings,group_val,gender)
     
            # if(enter>exit):      
            #     detected = enter - exit
                        
            cv2.rectangle(frame,(x3,y3),(x4,y4),(255,0,0),1)
            cv2.circle(frame,(x_centre,y_centre),4,(255,0,0),-1)
            cv2.putText(frame,str(int(id)),(x3,y3),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,0,0),1)
            cv2.putText(frame,gender_label,((x3+19),y3),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,0,0),1)
        
    #     cv2.imshow("RGB", frame)
    #     if cv2.waitKey(1)&0xFF==27:
    #         break
    # cap.release()
    # cv2.destroyAllWindows()


def clear_lists():
    global counter1, counter2
    counter1 = []
    counter2 = []
    print("Lists cleared")                    


#For encoding person
def encode_face_image(image):
    encoding = face_recognition.face_encodings(image)
    if not encoding:
        print("Person image not clear")
        return None

    # Return the encoding of the first face
    return encoding[0]


def calculate_distance(coord1, coord2):
    x1, y1, x2, y2 = coord1
    x3, y3, x4, y4 = coord2
    cx1 = (x1 + x2) // 2
    cy1 = (y1 + y2) // 2
    cx2 = (x3 + x4) // 2
    cy2 = (y3 + y4) // 2
    return math.sqrt((cx1 - cx2) ** 2 + (cy1 - cy2) ** 2)

def group_coordinates(coordinates, group_threshold):
    # Dictionary to store the groups
    coordinate_groups = {}

    # Iterate through each set of coordinates
    for i, coord_data in enumerate(coordinates):
        person_id = coord_data['id']
        coord = coord_data['coord']
        # Flag to check if the coordinates have been added to a group
        added_to_group = False

        # Iterate through existing groups to check for proximity
        for group_key, group_data in coordinate_groups.items():
            for group_coord_data in group_data:
                dist = calculate_distance(coord, group_coord_data['coord'])

                # If the coordinates are close enough to any coordinates in the group, add them to the group
                if dist < group_threshold:
                    coordinate_groups[group_key].append({'id': person_id, 'coord': coord})
                    added_to_group = True
                    break  # No need to check other groups

            if added_to_group:
                break  # No need to check other groups

        # If the coordinates were not added to any existing group, create a new group for them
        if not added_to_group:
            coordinate_groups[i] = [{'id': person_id, 'coord': coord}]  # Assign a unique key for the new group

    return coordinate_groups

def process_groups(coordinate_groups):
    group_status = {}
    for group_key, group_members in coordinate_groups.items():
        if len(group_members) >= 2:
            for member_data in group_members:
                member_id = member_data['id']
                group_status[member_id] = True  # In a group
        else:
            for member_data in group_members:
                member_id = member_data['id']
                group_status[member_id] = False  # Not in a group
                
    return group_status
                
         
         
           
# processing()