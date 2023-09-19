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
def calculate_distance(cen1, cen2):
    x1, y1 = cen1
    x2, y2 = cen2
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)



def group_centroids(centroids, group_threshold):
    # Create an empty dictionary to store the groups
    centroid_groups = {}

    # Iterate through each centroid
    for i, centroid in enumerate(centroids):
        # Flag to check if the centroid has been added to a group
        added_to_group = False

        # Iterate through existing groups to check for proximity
        for group_key, group_centroids in centroid_groups.items():
            for group_centroid in group_centroids:
                dist = calculate_distance(centroid, group_centroid)

                # If the centroid is close enough to any centroid in the group, add it to the group
                if dist < group_threshold:
                    centroid_groups[group_key].append(centroid)
                    added_to_group = True
                    break  # No need to check other groups

            if added_to_group:
                break  # No need to check other groups

        # If the centroid was not added to any existing group, create a new group for it
        if not added_to_group:
            centroid_groups[i] = [centroid]  # Assign a unique key for the new group

    return centroid_groups



group_threshold = 30 # Adjust this threshold based on your scenario


while True:
    ret, frame = cap.read()
    if not ret:
        break
    # count += 1
    # if count % 3 != 0:
    #     continue

    frame = cv2.resize(frame, (1020, 500))

    conf_thresh = 0.1

    results = model.predict(frame, classes=[0])
    a = results[0].boxes.data
    px = pd.DataFrame(a).astype("float")
    #list = []
    centroids = []
    #distances = []

    for index, row in px.iterrows():
        x1 = int(row[0])
        y1 = int(row[1])
        x2 = int(row[2])
        y2 = int(row[3])
        d = int(row[5])
        cx = int(x1 + x2) // 2
        cy = int(y1 + y2) // 2
        centroids.append([cx, cy])
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 225, 0), 2)  # Draw individual bounding boxes

    centroid_groups = group_centroids(centroids, group_threshold)
    print(centroid_groups)

    grpCount = 0
    # Iterate through the grouped centroids and draw bounding boxes around groups
    for group_key, group_cent in centroid_groups.items():
        if len(group_cent) >= 2:
            print("Group detected, key:",group_key)
            grpCount = grpCount + 1
            min_x = min([cx for (cx, cy) in group_cent])
            min_y = min([cy for (cx, cy) in group_cent])
            max_x = max([cx for (cx, cy) in group_cent])
            max_y = max([cy for (cx, cy) in group_cent])
            cv2.rectangle(frame, (min_x, min_y), (max_x, max_y), (0, 0, 0), 2)

    print("Group Count: ",grpCount)        
            

    cv2.imshow("RGB", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break


cap.release()
cv2.destroyAllWindows()

