import cv2
import pandas as pd
import numpy as np
from ultralytics import YOLO
from tracker import Tracker
from deepface import DeepFace
from flask import Flask, jsonify, Response
from flask_cors import CORS
import base64
from datetime import datetime
import threading

app = Flask(__name__)
CORS(app)

model = YOLO('yolov8s.pt')

# def RGB(event, x, y, flags, param):
#     if event == cv2.EVENT_MOUSEMOVE:
#         colorsBGR = [x, y]
#         print(colorsBGR)

# cv2.namedWindow('RGB')
# cv2.setMouseCallback('RGB', RGB)

cap = cv2.VideoCapture('H:\\Downloads\\rtsp___172.23.16.150_554 - VLC media player 2023-10-16 12-56-14.mp4')

my_file = open("coco.txt", "r")
data = my_file.read()
class_list = data.split("\n")

count = 0
detected = 0
tracker = Tracker()

latest_frame = None
frame_lock = threading.Lock()
male = 0
female = 0
unknown = 0

groupCount = 0

people_enter = {}
counter1 = []
enter = 0
exit = 0

people_exit = {}
counter2 = []

people_in_frame = 0

#Gate 1
area1=[(241,164),(332,173),(326,187),(234,171)]
area2=[(248,150),(344,157),(339,171),(242,159)]

#Gate 2
area3=[(602,206),(695,221),(702,232),(602,218)]
area4=[(606,183),(691,196),(693,212),(602,198)]


def compute_data():
    global cap
    global latest_frame
    global male
    global female
    global unknown
    global detected
    global count
    global enter
    global exit
    global people_enter
    global people_exit
    global counter1
    global counter2
    global people_in_frame
    
    while True:

        if not cap:
            cap = cv2.VideoCapture('rtsp://admin:Ncsael-123@172.23.16.150:554')

        ret, frame = cap.read()
        if not ret:
            print("Error reading frame. Reopening the stream...")
            cap.release()
            cap = None
            continue

        count += 1
        if count % 3 != 0:
            continue

        frame = cv2.resize(frame, (1020, 500))
        # Gate 1
        cv2.polylines(frame, [np.array(area1, np.int32)], True, (0, 0, 255), 1)
        cv2.polylines(frame, [np.array(area2, np.int32)], True, (0, 255, 0), 1)
        # Gate 2
        cv2.polylines(frame, [np.array(area3, np.int32)], True, (0, 0, 255), 1)
        cv2.polylines(frame, [np.array(area4, np.int32)], True, (0, 255, 0), 1)

        conf = 0.5

        results = model.predict(frame, conf=0.3, classes=[0])
        #   print(results)
        a = results[0].boxes.data
        px = pd.DataFrame(a).astype("float")
        #    print(px)
        list = []
        for index, row in px.iterrows():

            x1 = int(row[0])
            y1 = int(row[1])
            x2 = int(row[2])
            y2 = int(row[3])
            d = int(row[5])

            list.append([x1, y1, x2, y2])

        bbox_id = tracker.update(list)
        people_in_frame = len(bbox_id)
        for bbox in bbox_id:
            x3, y3, x4, y4, id = bbox
            x_centre = (x3 + x4) // 2

            face = frame[y3:y4, x3:x4]
            # GATE 1

            # people leave
            # result is 1 if person inside that area and -1 if person isn't inside the area
            results1 = cv2.pointPolygonTest(np.array(area1, np.int32), ((x_centre, y4)), False)
            if results1 >= 0:
                people_exit[id] = (x4, y4)
            if id in people_exit:
                results2 = cv2.pointPolygonTest(np.array(area2, np.int32), ((x_centre, y4)), False)
                if results2 >= 0:
                    if counter2.count(id) == 0:
                        counter2.append(id)
                        exit = exit + 1
                        if detected != 0:
                            detected = detected - 1
                        print("Exit count: ", len(counter2))

            # People Enter
            results3 = cv2.pointPolygonTest(np.array(area2, np.int32), ((x_centre, y4)), False)
            if results3 >= 0:
                # print("result3:",results3)
                people_enter[id] = (x4, y4)
            if id in people_enter:
                results4 = cv2.pointPolygonTest(np.array(area1, np.int32), ((x_centre, y4)), False)
                if results4 >= 0:
                    if counter1.count(id) == 0:
                        counter1.append(id)
                        detected = detected + 1
                        enter = enter + 1
                        #cv2.imshow("Detected faces", face)
                        # Gender detection
                        try:
                            gender_result = DeepFace.analyze(face, actions=['gender'])
                            gender = gender_result['gender']
                            print("Here")
                            if gender == 'Male':
                                with frame_lock:
                                    male = male + 1
                            elif gender == 'Female':
                                with frame_lock:
                                    female = female + 1
                        except Exception as e:
                            gender = 'Unknown'
                            with frame_lock:
                                unknown = unknown + 1
                            print(e)

                        print("GENDER: ", gender)
                        print("Enter count: ", len(counter1))

            # GATE 2
            # People Leave
            results5 = cv2.pointPolygonTest(np.array(area3, np.int32), ((x_centre, y4)), False)
            if results5 >= 0:
                people_exit[id] = (x4, y4)
            if id in people_exit:
                results6 = cv2.pointPolygonTest(np.array(area4, np.int32), ((x_centre, y4)), False)
                if results6 >= 0:
                    if counter2.count(id) == 0:
                        counter2.append(id)
                        exit = exit + 1
                        if detected != 0:
                            detected = detected - 1
                        print("Exit count: ", len(counter2))

            # People Enter
            results7 = cv2.pointPolygonTest(np.array(area4, np.int32), ((x_centre, y4)), False)
            if results7 >= 0:
                # print("result3:",results3)
                people_enter[id] = (x4, y4)
            if id in people_enter:
                results8 = cv2.pointPolygonTest(np.array(area3, np.int32), ((x_centre, y4)), False)
                if results8 >= 0:
                    if counter1.count(id) == 0:
                        counter1.append(id)
                        detected = detected + 1
                        enter = enter + 1
                        try:
                            gender_result = DeepFace.analyze(face, actions=['gender'])
                            gender = gender_result['gender']
                            if gender == 'Male':
                                with frame_lock:
                                    male = male + 1
                            elif gender == 'Female':
                                with frame_lock:
                                    female = female + 1

                        except Exception as e:
                            gender = 'Unknown'
                            with frame_lock:
                                unknown = unknown + 1
                        print("Enter count: ", len(counter1))

            with frame_lock:
                latest_frame = frame
            # print("Detected people: ",detected)
            cv2.rectangle(frame, (x3, y3), (x4, y4), (255, 0, 255), 1)
            cv2.circle(frame, (x_centre, y4), 4, (255, 0, 0), -1)
            cv2.putText(frame, str(int(id)), (x3, y3), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0), 1)
            # Entry
            cv2.putText(frame, f"Entry: {str(enter)}", (30, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1)
            # Exit
            cv2.putText(frame, f"Exit: {str(exit)}", (30, 125), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1)
            # Gender
            cv2.putText(frame, f"Male: {str(male)}", (30, 150), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
            cv2.putText(frame, f"Female: {str(female)}", (30, 175), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
            cv2.putText(frame, f"Unknown: {str(unknown)}", (30, 200), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)

        # cv2.imshow("RGB", frame)
        # if cv2.waitKey(1) & 0xFF == 27:
        #     break

    cap.release()
    cv2.destroyAllWindows()


@app.route('/get_data/<int:group_threshold>', methods=['GET'])
def get_data(group_threshold):
    global latest_frame
    global male
    global female
    global unknown
    global detected
    with frame_lock:
        if latest_frame is None:
            return Response('Error: No frame available', status=500)

        _, encoded_frame = cv2.imencode('.jpg', latest_frame)

        if encoded_frame is None:
            print("Error here")
            return Response('Error: Unable to encode frame', status=500)

        frame_bytes = base64.b64encode(encoded_frame)
        timestamp = datetime.now().strftime('%H:%M:%S')
        response_data = {
            'count': people_in_frame,
            'frame': frame_bytes.decode('utf-8'),  # Convert bytes to a string
            'groupCount': groupCount,
            'time': timestamp,
            'male': male,
            'female': female,
            'unknown': unknown
        }
    return jsonify(response_data)


if __name__ == '__main__':
    thread = threading.Thread(target=compute_data)
    thread.start()
    app.run(host='192.168.100.10', port=8080)
