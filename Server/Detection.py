import cv2
import pandas as pd
import numpy as np
from ultralytics import YOLO
from tracker import *
from deepface import DeepFace


model=YOLO('yolov8s.pt')


def RGB(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE :  
        colorsBGR = [x, y]
        print(colorsBGR)
        

cv2.namedWindow('RGB')
cv2.setMouseCallback('RGB', RGB)

cap=cv2.VideoCapture('H:\\Downloads\\people2\\people2.mp4')


my_file = open("coco.txt", "r")
data = my_file.read()
class_list = data.split("\n")
#print(class_list)
count=0
tracker=Tracker()   


while True:    
    ret,frame = cap.read()
    if not ret:
        break
    count += 1
    if count % 3 != 0:
        continue


    frame=cv2.resize(frame,(1020,500))
    
    conf_thresh = 0.5

    results=model.predict(frame,classes=[0])
 #   print(results)
    a=results[0].boxes.data
    px=pd.DataFrame(a).astype("float")
#    print(px)
    list=[]
    for index,row in px.iterrows():
#        print(row)
 
        x1=int(row[0])
        y1=int(row[1])
        x2=int(row[2])
        y2=int(row[3])
        d=int(row[5])
        #c=class_list[d]
    
        list.append([x1,y1,x2,y2])
            
    bbox_idx=tracker.update(list)
    
    
    for bbox in bbox_idx:
        x3,y3,x4,y4,id=bbox
        face = frame[y3:y4, x3:x4]
    
        cv2.imshow("Face",face)
        if cv2.waitKey(0)&0xFF==27:
            break
        try:
            gender_result = DeepFace.analyze(face, actions=['gender'])
            gender = gender_result['gender']
        except Exception as e:
            gender='Unknown'
        print(gender)
        cx=int(x3+x4)//2
        cy=int(y3+y4)//2
        cv2.rectangle(frame,(x3,y3),(x4,y4),(0,255,0),2)
        cv2.putText(frame,str(int(id)),(x3,y3),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,0,0),1)
        cv2.putText(frame,str(gender),(x3,(y3+5)),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,0,0),1)
        
           
    cv2.imshow("RGB", frame)
    if cv2.waitKey(0)&0xFF==27:
        break
cap.release()
cv2.destroyAllWindows()