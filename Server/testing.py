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
    image_path="C:\\Users\\Hareem\\Desktop\\nM5rWKDQpTRpd8umswYMz0eFZ0EDfHKXXPPv6a0xw8s=_plaintext_638356738756599786.jpg"
    encoding = encode_face_image(image_path)
    gender = "Male"  # Replace with the actual gender
    group_val = True  # Replace with the actual group value

    # Add customer and visit
    customer_exist(encoding, group_val, gender)
    print("Done")

    # Simulate customer leaving
    # Assuming that after some time, the customer is leaving, and you want to update the visit with the time_out
    # customer_leaving(encoding)

# Run the testing code
test_functions()
