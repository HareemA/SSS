import cv2
from mtcnn.mtcnn import MTCNN

# Load MTCNN
mtcnn = MTCNN()

# Open video file
cap = cv2.VideoCapture('H:\\Downloads\\rtsp___172.23.16.150_554 - VLC media player 2023-10-16 12-56-14.mp4')

while True:
    # Read a frame from the video
    ret, frame = cap.read()

    # Check if the frame was read successfully
    if not ret:
        break  

    frame = cv2.resize(frame, (1020, 500))
    # Detect faces using MTCNN
    faces = mtcnn.detect_faces(frame)

    # Draw bounding boxes around detected faces
    for face in faces:
        x, y, width, height = face['box']
        cv2.rectangle(frame, (int(x), int(y)), (int(x+width), int(y+height)), (0, 255, 0), 2)

    # Display the result
    cv2.imshow('Face Detection using MTCNN', frame)

    # Break the loop when 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()
