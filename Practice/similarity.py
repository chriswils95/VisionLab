
"""
Title: similarity.py
Author: Christopher Wilson
Group: IMMERSE  NSO Life

    This file contains the class code for the similarity face playground.
    The class import the similarity UI Winodws, and take care of the 
    functionalities of the playground


###########################################################################################################################
###   LIBRARIES   ###   LIBRARIES   ###   LIBRARIES   ###   LIBRARIES   ###   LIBRARIES   ###   LIBRARIES   ###   LIBRARIES
###########################################################################################################################
"""
from similarity_window1 import Ui_MainWindow
from ai import Ai_MainWindow
from app import App
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget
from PyQt5.QtGui import QPalette, QBrush, QPixmap, QMovie, QScreen
from PyQt5.QtCore import pyqtSignal, QThread, QTimer, QEventLoop
from PyQt5.QtCore import Qt
import PyQt5.QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import threading
from PyQt5.Qt import QImage, Qt
import sys
import cv2
import os
import tkinter as tk
import global_class 
from PyQt5.QtGui import QPixmap, QPainter
from Basic_stylesheet import main_stylesheet
import face_recognition

import cv2

import pickle


import numpy as np




"""
########################################################################################################################
###   SIMILARITY FACE PLAYGROUND CLASS   ###   SIMILARITY FACE PLAYGROUND CLASS   ###   SIMILARITY FACE PLAYGROUND CLASS
########################################################################################################################
"""
class Similarity_window(QtWidgets.QMainWindow, Ui_MainWindow):
  def __init__(self, parent):
        super().__init__()

        #setup the playground window
        self.setupUi(self)

        #assigns the main window to parent, useful in redirect back to main window
        self.parent = parent
        self.camera = global_class.camera
        self.shadow = QGraphicsDropShadowEffect()
        self.is_training = False
        self.stop.clicked.connect(self.stop_live)
        self.start.clicked.connect(self.start_live)
        self.reset.clicked.connect(self.reset_live)
        self.sPath = "/home/christopher/NSO_LIFE/Church_leaders"
        # setting blur radius 
        self.shadow.setBlurRadius(10) 
        # adding shadow to the label 
        self.frame.setGraphicsEffect(self.shadow) 
        self.frame_2.setGraphicsEffect(self.shadow) 
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.nextFrameSlot)
        self.timer.start(1000./24)



  """ This function finds the image that corresponds to the given image name"""
  def find_image(self, name):
   for roots, dirs, files in os.walk(self.sPath):
     for file in files:
       temp = file.split(".")
       if(temp[0] == name):
         return file


  """This function puts the camera frames into a QLabel"""
  def nextFrameSlot(self):
   ret, self.frame = self.camera.read()
   self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)

   #only show the similar face image if is training is true
   if(self.is_training):
    self.name = ""
    self.frame, self.name = self.apply_training(self.frame)
    similar_face_image = self.find_image(self.name)
    if(similar_face_image is not None):
     similar_face_pixmap = QPixmap(self.sPath + "/" + similar_face_image)
     self.live_label.setPixmap(similar_face_pixmap)
    img = QtGui.QImage(self.frame, self.frame.shape[1], self.frame.shape[0], QtGui.QImage.Format_RGB888)
    pix = QtGui.QPixmap.fromImage(img)
    self.train_label.setPixmap(pix)
   else:
    img = QtGui.QImage(self.frame, self.frame.shape[1], self.frame.shape[0], QtGui.QImage.Format_RGB888)
    pix = QtGui.QPixmap.fromImage(img)
    self.train_label.setPixmap(pix)


  """
  This fucntion checks to see is the escape key is pressed, close this window
  and open the parent window
  """
  def keyPressEvent(self, event):
    key = event.key()
    if key == Qt.Key_Escape:
     self.timer.stop()
     self.close()
     self.parent.showFullScreen()

  
## This function stops the training
  def stop_live(self):
    self.stop.setStyleSheet("QPushButton { background-color: red }")
    self.reset.setStyleSheet("QPushButton { background-color: white }")
    self.start.setStyleSheet("QPushButton { background-color: white }")
    self.is_training = False
    print("stop")
  
## THis function starts the ai training
  def start_live(self):
    self.start.setStyleSheet("QPushButton { background-color: green }")
    self.reset.setStyleSheet("QPushButton { background-color: white }")
    self.stop.setStyleSheet("QPushButton { background-color: white }")
    self.is_training = True
    print("start")

##This function also stops the training but resets the colors and images
  def reset_live(self):
   self.reset.setStyleSheet("QPushButton { background-color: white }")
   self.stop.setStyleSheet("QPushButton { background-color: white }")
   self.start.setStyleSheet("QPushButton { background-color: white }")
   self.is_training = False
   print("reset")
  

 ## This function is responsible for ai training
  def apply_training(self, frame):
   ##Loads the known celebrity faces in bytes form in data
   self.data = pickle.loads(open("/home/christopher/NSO_LIFE/celebrities_faces.pkl", "rb").read())
   self.data = np.array(self.data)
   self.known_face_encodings = self.data#[d["encoding"] for d in data]
   ##Loads the known celebrity names in bytes form in data
   self.data = pickle.loads(open("/home/christopher/NSO_LIFE/celebrities_names.pkl", "rb").read())
   self.known_face_names = self.data
   self.face_locations = []
   self.face_encodings = []
   self.face_names = []
   self.process_this_frame = True
    # Resize frame of video to 1/4 size for faster face recognition processing
   small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
   rgb_small_frame = small_frame[:, :, ::-1]
    # Only process every other frame of video to save time

   if self.process_this_frame:

        # Find all the faces and face encodings in the current frame of video

        self.face_locations = face_recognition.face_locations(rgb_small_frame)

        self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)



        self.face_names = []

        for face_encoding in self.face_encodings:

            # See if the face is a match for the known face(s)

            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding, tolerance=0.3)

            name = "Unknown"



            # # If a match was found in known_face_encodings, just use the first one.

            # if True in matches:

            #     first_match_index = matches.index(True)

            #     name = known_face_names[first_match_index]



            # Or instead, use the known face with the smallest distance to the new face

            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            
            counter = 0
            # for i in face_distances:
            #  counter = counter + 1
            #  print("distances at " + str(counter) + ": " + str(i))
            best_match_index = np.argmin(face_distances)
            
            print(best_match_index)

            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]
            else:
                name = self.known_face_names[best_match_index]



            self.face_names.append(name)



   self.process_this_frame = not self.process_this_frame

    # Display the results
   self.similar_face_name = ""
   for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):

        # Scale back up face locations since the frame we detected in was scaled to 1/4 size

        top *= 4

        right *= 4

        bottom *= 4

        left *= 4


        
        # Draw a box around the face

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)



        # Draw a label with a name below the face

        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)

        font = cv2.FONT_HERSHEY_DUPLEX

        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        self.similar_face_name = name


    # Display the resulting imag

   return frame, self.similar_face_name



    # Hit 'q' on the keyboard to quit!




# if __name__ == '__main__':
    
#   app = QApplication(sys.argv)
#   form = Window()
#   form.showFullScreen()
#   app.setStyleSheet(main_stylesheet)
#   app.exec_()