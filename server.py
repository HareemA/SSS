import cv2
import pandas as pd
import numpy as np
from ultralytics import YOLO
from tracker import *
from flask import Flask, jsonify, render_template, request, Response
import threading 

app = Flask(__name__)

model=YOLO('yolov8s.pt')


my_file = open("coco.txt", "r")
data = my_file.read()
class_list = data.split("\n")
#print(class_list)
count=0
tracker=Tracker()   


latest_frame = None  # Initialize a variable to store the latest frame
detected_persons_count = 0

@app.route('/update_frame', methods=['POST'])
def update_frame():
    global latest_frame,detected_persons_count

    try:
        frame_bytes = request.data

        if not frame_bytes:
            return Response('Error: Empty frame data', status=400)

        # Convert frame_bytes to a NumPy array
        frame_array = np.frombuffer(frame_bytes, np.uint8)

        # Decode the frame
        frame = cv2.imdecode(frame_array, cv2.IMREAD_COLOR)

    #     conf_thresh = 0.5

    #     results=model.predict(frame,classes=[0])
    # #   print(results)
    #     a=results[0].boxes.boxes
    #     px=pd.DataFrame(a).astype("float")
    # #    print(px)
    #     list=[]
    #     for index,row in px.iterrows():
    # #        print(row)
    
    #         x1=int(row[0])
    #         y1=int(row[1])
    #         x2=int(row[2])
    #         y2=int(row[3])
    #         d=int(row[5])
    #         #c=class_list[d]
        
    #         list.append([x1,y1,x2,y2])
                
    #     bbox_idx=tracker.update(list)
    #     detected_persons_count = len(bbox_idx)
        
    #     for bbox in bbox_idx:
    #         x3,y3,x4,y4,id=bbox
    #         cx=int(x3+x4)//2
    #         cy=int(y3+y4)//2
    #         cv2.rectangle(frame,(x3,y3),(x4,y4),(0,255,0),2)
    #         cv2.putText(frame,str(int(id)),(x3,y3),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,0,0),1)

        if frame is None:
            return Response('Error: Unable to decode frame', status=400)

        # Store the latest frame
        latest_frame = frame

        return Response('Frame received', status=200)
    except Exception as e:
        return Response(f'Error: {str(e)}', status=500)


@app.route('/get_latest_processed_frame', methods=['GET'])
def get_latest_processed_frame():
    global latest_frame
    global detected_persons_count
    try:
        if latest_frame is None:
            return Response('No processed frame available', status=404)
        
        frame = latest_frame

        conf_thresh = 0.5

        results=model.predict(frame,classes=[0])
    #   print(results)
        a=results[0].boxes.boxes
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
        detected_persons_count = len(bbox_idx)
        
        for bbox in bbox_idx:
            x3,y3,x4,y4,id=bbox
            cx=int(x3+x4)//2
            cy=int(y3+y4)//2
            cv2.rectangle(frame,(x3,y3),(x4,y4),(0,255,0),2)
            cv2.putText(frame,str(int(id)),(x3,y3),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,0,0),1)

        # Convert the processed frame to JPEG format
        #_, encoded_frame = cv2.imencode('.jpg', latest_frame)
        _, encoded_frame = cv2.imencode('.jpg', frame)

        if encoded_frame is None:
            print("Error here")
            return Response('Error: Unable to encode frame', status=500)

        frame_bytes = encoded_frame.tobytes()
        
        #be sure to decode frame on clients side
        response_data = {
            'count': detected_persons_count,
            'frame': frame_bytes.decode('latin1')  # Convert bytes to a string
        }
        return jsonify(response_data)

        #return Response(response=frame_bytes, status=200, mimetype='image/jpeg')

       
    except Exception as e:
        print(e)
        return Response(f'Error: {str(e)}', status=500)




if __name__ == '__main__':
    app.run(host='192.168.18.132',port=8080)

    
