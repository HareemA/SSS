import cv2
from deepface import DeepFace

imgpath = 'faces/face.jpg'

# Load the image using cv2.imread
img = cv2.imread(imgpath)

# Check if the image is successfully loaded
if img is not None:
    # Resize the image
    size = (150, 150)
    resized_img = cv2.resize(img, size)

    # Histogram Equalization
    equalized_img = cv2.equalizeHist(resized_img)

    # Gaussian Blur
    blurred_img = cv2.GaussianBlur(equalized_img, (5, 5), 0)

    cv2.imshow("Face", blurred_img)

    # Analyze the face using DeepFace
    result = DeepFace.analyze(blurred_img, actions=['gender'])
    print(result)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print(f"Failed to load the image from '{imgpath}'")
