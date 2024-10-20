import time
import json

import cv2
import pickle
import face_recognition
import time


import numpy as np

def add_data(person):
    # Sample data (dictionary)
    data = {
        "name": f"{person}",
    }

    # Serialize the data to JSON
    json_data = json.dumps(data)

    # Write JSON data to a file
    with open("data.json", "w") as json_file:
        json_file.write(json_data)




print("Loading Encode File ... ")
file = open('EncodeFile.p','rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds



cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)



detection = -1

count = 0

while True:
    success, img = cap.read()

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    for encodeFace, faceLoc in zip(encodeCurFrame,faceCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
        index =0

        data =-1

        print(faceDis)

        index =0


        array_from_list = np.array(faceDis)

        min =0
        minvalue = array_from_list[0]

        for i in range( len(faceDis) ):

            if( minvalue > array_from_list[i] ):
                min = i
                minvalue = array_from_list[i]

        if( minvalue < 0.5 and min == detection   ):
            count= count + 1
        else :
            count =0
            detection = min
        
        if( count  > 3 ):
            print("crminal found")
            add_data("criminal found")





    cv2.imshow("criminal", img)
    cv2.waitKey(1)



cap.release()
cv2.destroyAllWindows()