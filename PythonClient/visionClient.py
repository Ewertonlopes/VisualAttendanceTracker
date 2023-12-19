import cv2
import requests
import numpy as np
import face_recognition
import csv
from datetime import datetime
import os

def get_filenames_without_extension(folder_path):
    file_names = []
    
    files = os.listdir(folder_path)
    
    for file in files:
        file_path = os.path.join(folder_path, file)
        
        if os.path.isfile(file_path):
            file_name, file_extension = os.path.splitext(file)

            file_names.append(file_name)
    
    return file_names

def equalize_color(img):
    frame_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)

    frame_yuv[:,:,0] = cv2.equalizeHist(frame_yuv[:,:,0])

    return cv2.cvtColor(frame_yuv, cv2.COLOR_YUV2BGR)

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_weekday():
    return datetime.now().strftime("%A")

def append_to_historic(file_path, name):
    timetag = get_timestamp()

    with open(file_path, 'a', newline='') as csvfile:

        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([get_weekday(),name, timetag])

def append_to_user(file_path, name,image):

    with open(file_path, 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

        csv_writer.writerow([name,image])

stream_url = "http://192.168.4.1:80"  

cap = cv2.VideoCapture(stream_url)

if not cap.isOpened():
    print("Error: Could not open video stream")
    exit()

Users = get_filenames_without_extension('Usuarios')
User_encod = []
Found_faces = []
for User in Users:
    u_image = face_recognition.load_image_file(f'Usuarios/{User}.jpg')
    u_encod = face_recognition.face_encodings(u_image) [0]
    User_encod.append(u_encod)

for i in range(len(Users)):
    Found_faces.append(False)    
 



counter = 1
while True:
    ret, frame = cap.read()

    if not ret:
        print("Error reading frame from the video stream")
        break
    
    frame_output = equalize_color(frame)

    face_locations = face_recognition.face_locations(frame_output,1,"hog")
    face_encodings = face_recognition.face_encodings(frame_output, face_locations,model='small')
    
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):

        matches = face_recognition.compare_faces(User_encod, face_encoding)

        name = "Unknown"
        
        face_distances = face_recognition.face_distance(User_encod, face_encoding)
        best_match_index = np.argmin(face_distances)

        if matches[best_match_index]:
            name = Users[best_match_index]
            found = Found_faces[best_match_index]

            if not found:
                csv_file_path = 'historic.csv'
                # Call the function to append data to the CSV file
                append_to_historic(csv_file_path, name)

                Found_faces[best_match_index] = True

    cv2.imshow('Video', frame_output)

    key = cv2.waitKey(1)

    if  key == ord('q'):
        break
    # elif key == ord('c'):
    #     name = input()
    #     image = f'res/image_1.jpg'
    #     cv2.imwrite(image,frame_output)
    #     append_to_user('users.csv',name,image)


cap.release()
cv2.destroyAllWindows()
