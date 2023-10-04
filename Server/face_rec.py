# import cv2
# from deepface import DeepFace
# import requests
# import cv2
# from pytube import YouTube

# def get_gender_count():
#     # YouTube video URL
#     youtube_url = 'https://youtu.be/P0wNIsAjht8?si=u1aedqcQSJfJq3U1'

#     yt = YouTube(youtube_url)

#     # Get the stream with the highest resolution
#     stream = yt.streams.get_highest_resolution()

#     # OpenCV VideoCapture from the stream URL
#     cap = cv2.VideoCapture(stream.url)

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break

#         # Analyze the image to detect gender
#         results = DeepFace.analyze(frame, actions=["gender"])

#         # Loop through the detected faces and draw boxes
#         for face in results:
#             x, y, w, h = face["region"]["x"], face["region"]["y"], face["region"]["w"], face["region"]["h"]
#             gender = "Male" if face["dominant_gender"] == "Man" else "Female"
#             cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Draw a green rectangle around the face
#             cv2.putText(frame, gender, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)  # Display gender label

#         # Display the frame with boxes and labels
#         cv2.imshow("Gender Detection", frame)

#         # Wait for a key press and then close the window
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#     cv2.destroyAllWindows()

# # Call the function to get gender count and display the result
# get_gender_count()



# # import cv2
# # from group_test_server import *

# # def detect_face():
# #     img = cv2.imread('faces/test2.jpg')
# #     frame , count , grp_count = main(img,0)

# #     cv2.imshow("Frame",frame)
# #     print(count)

# #     cv2.waitKey(0)
# #     cv2.destroyAllWindows()

# # detect_face()
