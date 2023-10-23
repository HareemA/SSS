import cv2
from deepface import DeepFace
import numpy as np

imgpath = 'faces/face2.jpg'

# Load the image using cv2.imread
img = cv2.imread(imgpath)
rows, cols = img.shape[:2]

# Check if the image is successfully loaded
if img is not None:

    result = DeepFace.analyze(img, actions=['gender'])
    print(result)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print(f"Failed to load the image from '{imgpath}'")
