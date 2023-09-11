import cv2
import requests
import numpy as np

server_url = 'http://192.168.18.132:8080/get_latest_processed_frame'  # Replace with the correct server URL

while True:
    try:
        response = requests.get(server_url)

        if response.status_code == 200:
            response_data = response.json()

            # Extract the count and frame data from the JSON response
            count = response_data['count']
            frame_bytes = response_data['frame'].encode('latin1')

            frame_array = np.frombuffer(frame_bytes, np.uint8)
            frame = cv2.imdecode(frame_array, cv2.IMREAD_COLOR)


            if frame is not None:
                cv2.putText(frame, f'Count: {count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                print("Count:",count)

                cv2.imshow('Latest Processed Frame', frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                print('Error: Unable to decode frame')
        elif response.status_code == 404:
            print('No processed frame available')
        else:
            print('Error:', response.status_code)

    except Exception as e:
        print('Error:', str(e))

cv2.destroyAllWindows()
