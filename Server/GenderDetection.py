import cv2
import pandas as pd
import numpy as np
from ultralytics import YOLO
from tracker import*
from deepface import DeepFace
import os
import face_recognition
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array

model=YOLO('yolov8n.pt')

gender_model = load_model('gender_detection.model')
classes = ['man', 'woman']

def RGB(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE :  
        colorsBGR = [x, y]
        print(colorsBGR)
        

cv2.namedWindow('RGB')
cv2.setMouseCallback('RGB', RGB)

cap = cv2.VideoCapture('H:\\Downloads\\vid2 - Trim.mp4')

# my_file = open("coco.txt", "r")
# data = my_file.read()
# class_list = data.split("\n") 

count=0
detected = 0
tracker=Tracker()

folder_name='data'
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Gate 1
# area1=[(241,164),(332,173),(326,187),(234,171)]
# area2=[(248,150),(344,157),(339,171),(242,159)]

# Gate 2
# area3=[(602,206),(695,221),(702,232),(602,218)]
# area4=[(606,183),(691,196),(693,212),(602,198)]

area1=[(135,186),(811,307),(802,342),(103,203)]
area2=[(176,159),(818,263),(812,301),(135,186)]

people_enter={}
counter1=[]
enter=0
exit=0

male=0
female=0
unknown=0

people_exit={}
counter2=[]

people = 0

while True:    
    ret,frame = cap.read()
    
    if not ret:
        break
    count += 1
    if count % 3 != 0:
        continue
    
    frame=cv2.resize(frame,(1020,500))
    
    original_coordinates = []  
    group_threshold = 50
        
    #Gate 1
    cv2.polylines(frame,[np.array(area1,np.int32)],True,(0,0,255),1)
    cv2.polylines(frame,[np.array(area2,np.int32)],True,(0,255,0),1)   
    #Gate 2
    # cv2.polylines(frame,[np.array(area3,np.int32)],True,(0,0,255),1)
    # cv2.polylines(frame,[np.array(area4,np.int32)],True,(0,255,0),1)   

    results=model.track(frame, conf = 0.3,classes=[0],persist=True)
    a=results[0].boxes.data
    px=pd.DataFrame(a).astype("float")
    
    gender_label = 'none'

    list=[]         
    for index,row in px.iterrows():
        x3=int(row[0])
        y3=int(row[1])
        x4=int(row[2])
        y4=int(row[3])
        d=int(row[5])
        id = int(row[4])
        # list.append([x1,y1,x2,y2])

    # bbox_id=tracker.update(list)
    # for bbox in bbox_id:
    #     x3,y3,x4,y4=bbox
        x_centre= (x3+x4)//2
        y_centre=(y3+y4)//2
        
        original_coordinates.append([x3, y3, x4, y4])
        
        person=frame[y3:y4,x3:x4]
        face_crop = cv2.resize(person, (96, 96))
        face_crop = face_crop.astype("float") / 255.0
        face_crop = img_to_array(face_crop)
        face_crop = np.expand_dims(face_crop, axis=0)

        gender_confidence = gender_model.predict(face_crop)[0]
        gender_index = np.argmax(gender_confidence)
        gender_label = classes[gender_index]
        #GATE 1

        #people leave
        #result is 1 if rerson inside that area and -1 if person isnt inside the area
        #x _centre,y4
        results1 = cv2.pointPolygonTest(np.array(area1,np.int32),((x_centre,y_centre)),False)
        if results1>=0:
            people_exit[id]=(x4,y4)
        if id in people_exit:
            results2 = cv2.pointPolygonTest(np.array(area2,np.int32),((x_centre,y_centre)),False)
            if results2>=0:
                if counter2.count(id)==0:
                    counter2.append(id)
                    exit=exit+1
                    detected = detected - 1
                    print("Exit count: ",len(counter2))

        #People Enter
        results3 = cv2.pointPolygonTest(np.array(area2,np.int32),((x_centre,y_centre)),False)
        if results3>=0:
            #print("result3:",results3)
            people_enter[id]=(x4,y4)
        if id in people_enter:
            results4 = cv2.pointPolygonTest(np.array(area1,np.int32),((x_centre,y_centre)),False)
            if results4>=0:
                if counter1.count(id)==0:
                    counter1.append(id)
                    detected = detected + 1
                    enter=enter+1
                    if gender_label == 'man':
                        male = male + 1
                    elif gender_label == 'woman':
                        female = female + 1
                    else:
                        print(gender_label)
                        unknown = unknown + 1

                    #     file_name = os.path.join(folder_name,f'face_{people}.jpg')
                    #     cv2.imwrite(file_name,face)

                    print("Enter count: ",len(counter1))



        #GATE 2
        #People Leave
        # results5 = cv2.pointPolygonTest(np.array(area3,np.int32),((x_centre,y4)),False)
        # if results5>=0:
        #     people_exit[id]=(x4,y4)
        # if id in people_exit:
        #     results6 = cv2.pointPolygonTest(np.array(area4,np.int32),((x_centre,y4)),False)
        #     if results6>=0:
        #         if counter2.count(id)==0:
        #             counter2.append(id)
        #             exit=exit+1
        #             detected = detected - 1
        #             print("Exit count: ",len(counter2))

        # #People Enter
        # results7 = cv2.pointPolygonTest(np.array(area4,np.int32),((x_centre,y4)),False)
        # if results7>=0:
        #     #print("result3:",results3)
        #     people_enter[id]=(x4,y4)
        # if id in people_enter:
        #     results8 = cv2.pointPolygonTest(np.array(area3,np.int32),((x_centre,y4)),False)
        #     if results8>=0:
        #         if counter1.count(id)==0:
        #             counter1.append(id)
        #             detected = detected + 1
        #             enter=enter+1
        #             try:
        #                 gender_result = DeepFace.analyze(face,actions=['gender'])
        #                 gender= gender_result['gender']
        #                 if gender=='Male':
        #                     male=male+1
        #                 elif gender=='Female':
        #                     female=female+1
                        
        #             except Exception as e:
        #                 gender='Unknown'
        #                 unknown= unknown +1
        #             print("Enter count: ",len(counter1))

        #print("Detected people: ",detected)
        cv2.rectangle(frame,(x3,y3),(x4,y4),(255,0,0),1)
        cv2.circle(frame,(x_centre,y_centre),4,(255,0,0),-1)
        cv2.putText(frame,str(int(id)),(x3,y3),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,0,0),1)
        cv2.putText(frame,gender_label,((x3+19),y3),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,0,0),1)
        
    coordinate_groups = group_coordinates(original_coordinates, group_threshold)

    #Iterate through the grouped coordinates and draw bounding boxes around groups
    for group_key, group_coord in coordinate_groups.items():
        if len(group_coord) >= 2:
            #print("Group detected, key:", group_key)
            group_count = group_count + 1
            min_x = min([x1 for (x1, y1, x2, y2) in group_coord])
            min_y = min([y1 for (x1, y1, x2, y2) in group_coord])
            max_x = max([x2 for (x1, y1, x2, y2) in group_coord])
            max_y = max([y2 for (x1, y1, x2, y2) in group_coord])
            cv2.rectangle(frame, (min_x, min_y), (max_x, max_y), (0, 0, 255), 2)
    #Entry
    cv2.putText(frame, f"Entry: {str(enter)}", (30, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1)
    #Exit
    cv2.putText(frame, f"Exit: {str(exit)}", (30, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1)
    #Gender
    cv2.putText(frame,f"Male: {str(male)}",(30,140),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
    cv2.putText(frame,f"Female: {str(female)}",(30,160),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
    cv2.putText(frame,f"Unknown: {str(unknown)}",(30,180),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)

    cv2.imshow("RGB", frame)
    if cv2.waitKey(1)&0xFF==27:
        break

cap.release()
cv2.destroyAllWindows()
