import cv2
import pandas as pd
import numpy as np
from ultralytics import YOLO
from tracker import*
from deepface import DeepFace
import os
import face_recognition
import threading

frame_lock = threading.Lock()

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
    #dictionary to store the groups
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





