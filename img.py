import cv2
from imutils import paths
import face_recognition
import argparse
import pickle
import os
import numpy as np

import pickle as dill
 
# # scores = [('joe', 1), ('bill', 2), ('betty', 100)]
# # nscores = len(scores)
# # with open('high.pkl', 'ab') as f:
# #    _ = [dill.dump(score, f) for score in scores]
 
counter = 0
data = []
names = []
sPath = "/home/christopher/NSO_LIFE/Church_leaders"
with open('celebrities_faces.pkl', 'ab') as f:
 with open('celebrities_names.pkl', 'ab') as d:
  for roots, dirs, files in os.walk(sPath):
   for file in files:
    counter = counter + 1
    print("[INFO] processing image {}/{}".format(counter,
		 len(files)))

    image = face_recognition.load_image_file(sPath + "/" + file)
    encodings = face_recognition.face_encodings(image)
    if len(encodings) > 0:
          encodings = encodings[0]
    else:
         height, width, _ = image.shape
# location is in css order - top, right, bottom, left
         # face_location = (0, width, height, 0)
         # encodings = face_recognition.face_encodings(image, known_face_locations=[face_location])  
         print("No face found")

    data.append(encodings)
    file = file[:-1]
    file = file[:-1]
    file = file[:-1]
    file = file[:-1]
    print(file)
    names.append(file)
  dill.dump(names, d)
 dill.dump(data, f)
