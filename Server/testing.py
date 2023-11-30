import shutil
import os
import uuid
import datetime
import face_recognition
from database import *


# Define a function to encode a face image
def encode_face_image(image_path):
    image = face_recognition.load_image_file(image_path)
    encoding = face_recognition.face_encodings(image)[0]
    return encoding

def test_functions():

    # Add a new customer and visit
    image_path="C:\\Users\\Hareem\\Desktop\\4.jpg"
    encoding = encode_face_image(image_path)
    gender = "Male"  # Replace with the actual gender
    group_val = True  # Replace with the actual group value

    # Add customer and visit
    customer_exist(encoding, group_val, gender)
    #update_visit_time_out("86b18bf4-49d9-46a4-b7cf-3ab7f041ed49")
    print("Done")

    # Simulate customer leaving
    # Assuming that after some time, the customer is leaving, and you want to update the visit with the time_out
    # customer_leaving(encoding)

# Run the testing code
test_functions()
