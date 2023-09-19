import cv2
from deepface import DeepFace

img = cv2.imread("faces/3.jpg")

result = DeepFace.analyze(img,actions=("gender","age","emotion","race"))

print("Result: ",result)
