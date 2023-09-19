import cv2
import pandas as pd
import numpy as np
from ultralytics import YOLO
from tracker import *
import math

model = YOLO('yolov8s.pt')

def RGB(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        colorsBGR = [x, y]
        print(colorsBGR)

cv2.namedWindow('RGB')
cv2.setMouseCallback('RGB', RGB)

cap = cv2.VideoCapture('vidp.mp4')

my_file = open("coco.txt", "r")
data = my_file.read()
class_list = data.split("\n")

count = 0
tracker = Tracker()

timestamp = 0

# Using Euclidean distance
def calculate_distance(coord1, coord2):
    x1, y1, x2, y2 = coord1
    x3, y3, x4, y4 = coord2
    cx1 = (x1 + x2) // 2
    cy1 = (y1 + y2) // 2
    cx2 = (x3 + x4) // 2
    cy2 = (y3 + y4) // 2
    return math.sqrt((cx1 - cx2) ** 2 + (cy1 - cy2) ** 2)

def group_coordinates(coordinates, group_threshold):
    # Create an empty dictionary to store the groups
    coordinate_groups = {}

    # Iterate through each set of coordinates
    for i, coord in enumerate(coordinates):
        # Flag to check if the coordinates have been added to a group
        added_to_group = False

        # Iterate through existing groups to check for proximity
        for group_key, group_coordinates in coordinate_groups.items():
            for group_coord in group_coordinates:
                dist = calculate_distance(coord, group_coord)

                # If the coordinates are close enough to any coordinates in the group, add them to the group
                if dist < group_threshold:
                    coordinate_groups[group_key].append(coord)
                    added_to_group = True
                    break  # No need to check other groups

            if added_to_group:
                break  # No need to check other groups

        # If the coordinates were not added to any existing group, create a new group for them
        if not added_to_group:
            coordinate_groups[i] = [coord]  # Assign a unique key for the new group

    return coordinate_groups

group_threshold = 35  # Adjust this threshold based on your scenario

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (1020, 500))

    conf_thresh = 0.1

    results = model.predict(frame, classes=[0])
    a = results[0].boxes.data
    px = pd.DataFrame(a).astype("float")

    original_coordinates = []  # Store the original coordinates of objects
    list=[]

    for index, row in px.iterrows():
        x1 = int(row[0])
        y1 = int(row[1])
        x2 = int(row[2])
        y2 = int(row[3])
        list.append([x1,y1,x2,y2])
          # Store the original coordinates
        #cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 225, 0), 2)  # Draw individual bounding boxes

    bbox_idx=tracker.update(list)
    
    for bbox in bbox_idx:
        x3,y3,x4,y4,id=bbox
        cx=int(x3+x4)//2
        cy=int(y3+y4)//2
        original_coordinates.append([x3, y3, x4, y4])
        cv2.rectangle(frame,(x3,y3),(x4,y4),(0,255,0),2)
        cv2.putText(frame,str(int(id)),(x3,y3),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,0,0),1)
        

    coordinate_groups = group_coordinates(original_coordinates, group_threshold)
    print(coordinate_groups)

    grpCount = 0
    # Iterate through the grouped coordinates and draw bounding boxes around groups
    for group_key, group_coord in coordinate_groups.items():
        if len(group_coord) >= 2:
            print("Group detected, key:", group_key)
            grpCount = grpCount + 1
            min_x = min([x1 for (x1, y1, x2, y2) in group_coord])
            min_y = min([y1 for (x1, y1, x2, y2) in group_coord])
            max_x = max([x2 for (x1, y1, x2, y2) in group_coord])
            max_y = max([y2 for (x1, y1, x2, y2) in group_coord])
            cv2.rectangle(frame, (min_x, min_y), (max_x, max_y), (0, 0, 0), 2)

    print("Group Count: ", grpCount)

    cv2.imshow("RGB", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
