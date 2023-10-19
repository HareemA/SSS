import cv2
from deepface import DeepFace
import numpy as np

imgpath = 'faces/face.jpg'

# Load the image using cv2.imread
img = cv2.imread(imgpath)
rows, cols = img.shape[:2]

# Check if the image is successfully loaded
if img is not None:
    # Resize the image
    img = cv2.resize(img,(500,500))
    # kernel_25 = np.ones((25,25),np.float32)/625.0
    # output_kernel = cv2.filter2D(img,-1,kernel_25)
    gaussian_blur= cv2.GaussianBlur(img,(7,7),2)

    sharpened1 = cv2.addWeighted(img,7.5,gaussian_blur,-6.5,0)

    cv2.imshow("Face", sharpened1)

    # Analyze the face using DeepFace
    # result = DeepFace.analyze(img, actions=['gender'])
    # print(result)

    cv2.waitKey(0)
    #cv2.destroyAllWindows()
else:
    print(f"Failed to load the image from '{imgpath}'")
