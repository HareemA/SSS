import math
import cv2
import pandas as pd
import numpy as np
from ultralytics import YOLO
import threading

model=YOLO('yolov8n.pt')


count = group_count = 0

# area1=[(1,367),(800,357),(792,406),(1,403)]
area1=[(2,350),(815,356),(795,413),(3,413)]

group_threshold = 55

group_lock = threading.Lock()

# video_link = "rtsp://admin:hik@12345@172.23.16.55"
video_link = "H:\\Downloads\\26102023_4.mp4"

cap = cv2.VideoCapture(video_link)

def processing():
    
    global cap, count, area1, group_threshold, video_link, group_lock

    while True:    
        
        if not cap:
            cap = cv2.VideoCapture(video_link)

        ret,frame = cap.read()
            
        if not ret:
            cap.release()
            cap = None
            continue
        
        #Perform processing on every third frame
        count += 1
        if count % 3 != 0:
            continue
        
        #Resize frame to drwa the area for detection
        frame=cv2.resize(frame,(1020,500))
        
        original_coordinates = []  
        
        group_stat={}
        
        #Dfining areas for detection
        cv2.polylines(frame,[np.array(area1,np.int32)],True,(0,0,255),1) 

        #Track people in  group
        results=model.track(frame, conf = 0.3,classes=[0],persist=True)
        a=results[0].boxes.data
        px=pd.DataFrame(a).astype("float")
        
        #Iterate through all the  points to group them
        for index,row in px.iterrows():
            x3=int(row[0])
            y3=int(row[1])
            x4=int(row[2])
            y4=int(row[3])
            d=int(row[5])
            id = int(row[4])
            
            cv2.rectangle(frame,(x3,y3),(x4,y4),(255,0,0),1)
            cv2.putText(frame,str(int(id)),(x3,y3),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,0,0),1)
            
            #For group detection append every detected person's id and coordinates
            original_coordinates.append({'id': id, 'coord': [x3, y3, x4, y4]})
          
        #Pass the dictionary to a function along with group threshold
        with group_lock:
            coordinate_groups = group_coordinates(original_coordinates, group_threshold)
            
        #For drawing bounding boxes around groups
        # for group_key, group_data in coordinate_groups.items():
        #     if len(group_data) >= 2:
        #         min_x = min([coord['coord'][0] for coord in group_data])
        #         min_y = min([coord['coord'][1] for coord in group_data])
        #         max_x = max([coord['coord'][2] for coord in group_data])
        #         max_y = max([coord['coord'][3] for coord in group_data])
        
        #         cv2.rectangle(frame, (min_x, min_y), (max_x, max_y), (0, 0, 255), 2)
            
        #Send the information about groups to a function which returns a dictionary containing id of person and boolean value for
        #indicating if hes in a group or not
        group_stat=process_groups(coordinate_groups)
        print("Group_stat: ",group_stat)
        
        #Now iterate through all the points again to predict gender, perform facial rec and add in database etc.
        


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
                         
# processing()