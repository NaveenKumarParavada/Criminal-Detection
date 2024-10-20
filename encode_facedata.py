import json
import cv2
import face_recognition
import pickle
import os

folderpath = 'Criminals'

# Check if the folder exists
if not os.path.exists(folderpath):
    raise Exception(f"The folder '{folderpath}' does not exist.")


# List all files in the folder
pathlist = os.listdir(folderpath)
print("Files in folder:", pathlist)

imagelist = []
studentslist = []

# Read images and student names from the folder
for path in pathlist:
    img_path = os.path.join(folderpath, path)
    if os.path.isfile(img_path):
        img = cv2.imread(img_path)
        if img is not None:
            imagelist.append(img)
            studentslist.append(os.path.splitext(path)[0])
        else:
            print(f"Warning: Could not read image '{img_path}'.")
    else:
        print(f"Warning: '{img_path}' is not a valid file.")

print("Student list:", studentslist)

# Function to find encodings for a list of images
def findEncodings(imagesList):
    encodeList = []
    i =0
    for img in imagesList:
        i=i + 1
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodings = face_recognition.face_encodings(img_rgb)
        if encodings:
            encodeList.append(encodings[0])
        else:
            print("Warning: No faces found in one of the images.", i)
    return encodeList

print("Encoding in progress...")
encodeListKnown = findEncodings(imagelist)

if not encodeListKnown:
    raise Exception("No encodings found. Ensure that the images contain detectable faces.")

encodeListKnownWithIds = [encodeListKnown, studentslist]

print("Encoding Complete")

# Save encodings to a file
with open("EncodeFile.p", 'wb') as file:
    pickle.dump(encodeListKnownWithIds, file)

print("Encodings saved to 'EncodeFile.p'")
