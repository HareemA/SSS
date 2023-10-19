import cv2
import pandas as pd
import numpy as np
from ultralytics import YOLO
from tracker import*
from deepface import DeepFace

model=YOLO('yolov8s.pt')

def RGB(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE :  
        colorsBGR = [x, y]
        print(colorsBGR)
        

cv2.namedWindow('RGB')
cv2.setMouseCallback('RGB', RGB)

cap = cv2.VideoCapture('H:\\Downloads\\rtsp___172.23.16.150_554 - VLC media player 2023-10-16 12-56-14.mp4')

my_file = open("coco.txt", "r")
data = my_file.read()
class_list = data.split("\n") 

count=0
detected = 0
tracker=Tracker()

#For shoppingmall
# area1=[(708,239),(690,253),(945,334),(959,317)]
# area2=[(681,257),(677,265),(927,353),(937,342)]

#For People count1
# area1=[(305,388),(513,468),(494,482),(298,399)]
# area2=[(279,392),(250,397),(423,477),(454,469)]

#Gate 1
area1=[(241,164),(332,173),(326,187),(234,171)]
area2=[(248,150),(344,157),(339,171),(242,159)]

#Gate 2
area3=[(602,206),(695,221),(702,232),(602,218)]
area4=[(606,183),(691,196),(693,212),(602,198)]

people_enter={}
counter1=[]
enter=0
exit=0

male=0
female=0
unknown=0

people_exit={}
counter2=[]
while True:    
    ret,frame = cap.read()
    if not ret:
        break
    count += 1
    if count % 3 != 0:
        continue
    
    frame=cv2.resize(frame,(1020,500))
    #Gate 1
    cv2.polylines(frame,[np.array(area1,np.int32)],True,(0,0,255),1)
    cv2.polylines(frame,[np.array(area2,np.int32)],True,(0,255,0),1)   
    #Gate 2
    cv2.polylines(frame,[np.array(area3,np.int32)],True,(0,0,255),1)
    cv2.polylines(frame,[np.array(area4,np.int32)],True,(0,255,0),1)   

    conf = 0.5

    results=model.predict(frame, conf = 0.3,classes=[0])
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
        
        list.append([x1,y1,x2,y2])

    bbox_id=tracker.update(list)
    for bbox in bbox_id:
        x3,y3,x4,y4,id=bbox
        x_centre= (x3+x4)//2

        face=frame[y3:y4,x3:x4]
        #GATE 1

        #people leave
        #result is 1 if rerson inside that area and -1 if person isnt inside the area
        results1 = cv2.pointPolygonTest(np.array(area1,np.int32),((x_centre,y4)),False)
        if results1>=0:
            people_exit[id]=(x4,y4)
        if id in people_exit:
            results2 = cv2.pointPolygonTest(np.array(area2,np.int32),((x_centre,y4)),False)
            if results2>=0:
                if counter2.count(id)==0:
                    counter2.append(id)
                    exit=exit+1
                    detected = detected - 1
                    print("Exit count: ",len(counter2))

        #People Enter
        results3 = cv2.pointPolygonTest(np.array(area2,np.int32),((x_centre,y4)),False)
        if results3>=0:
            #print("result3:",results3)
            people_enter[id]=(x4,y4)
        if id in people_enter:
            results4 = cv2.pointPolygonTest(np.array(area1,np.int32),((x_centre,y4)),False)
            if results4>=0:
                if counter1.count(id)==0:
                    counter1.append(id)
                    detected = detected + 1
                    enter=enter+1
                    cv2.imshow("Detected faces",face)
                    #Gender detection
                    try:
                        gender_result = DeepFace.analyze(face,actions=['gender'])
                        gender= gender_result['gender']
                        print("Here")
                        if gender=='Male':
                            male=male+1
                        elif gender=='Female':
                            female=female+1
                    except Exception as e:
                        gender='Unknown'
                        unknown=unknown+1
                        print(e)

                    print("GENDER: ",gender)
                    print("Enter count: ",len(counter1))



        #GATE 2
        #People Leave
        results5 = cv2.pointPolygonTest(np.array(area3,np.int32),((x_centre,y4)),False)
        if results5>=0:
            people_exit[id]=(x4,y4)
        if id in people_exit:
            results6 = cv2.pointPolygonTest(np.array(area4,np.int32),((x_centre,y4)),False)
            if results6>=0:
                if counter2.count(id)==0:
                    counter2.append(id)
                    exit=exit+1
                    detected = detected - 1
                    print("Exit count: ",len(counter2))

        #People Enter
        results7 = cv2.pointPolygonTest(np.array(area4,np.int32),((x_centre,y4)),False)
        if results7>=0:
            #print("result3:",results3)
            people_enter[id]=(x4,y4)
        if id in people_enter:
            results8 = cv2.pointPolygonTest(np.array(area3,np.int32),((x_centre,y4)),False)
            if results8>=0:
                if counter1.count(id)==0:
                    counter1.append(id)
                    detected = detected + 1
                    enter=enter+1
                    try:
                        gender_result = DeepFace.analyze(face,actions=['gender'])
                        gender= gender_result['gender']
                        if gender=='Male':
                            male=male+1
                        elif gender=='Female':
                            female=female+1
                        
                    except Exception as e:
                        gender='Unknown'
                        unknown= unknown +1
                    print("Enter count: ",len(counter1))

        #print("Detected people: ",detected)
        cv2.rectangle(frame,(x3,y3),(x4,y4),(255,0,255),1)
        cv2.circle(frame,(x_centre,y4),4,(255,0,0),-1)
        cv2.putText(frame,str(int(id)),(x3,y3),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,0,0),1)
        #Entry
        cv2.putText(frame, f"Entry: {str(enter)}", (30, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 1)
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
