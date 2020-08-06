
"""
Title: app.py
Author: Christopher Wilson
Group: IMMERSE  NSO Life

    This file contains the class code for the object detection playground.
    The class import the ai UI Windows, and take care of the 
    functionalities of the playground


###########################################################################################################################
###   LIBRARIES   ###   LIBRARIES   ###   LIBRARIES   ###   LIBRARIES   ###   LIBRARIES   ###   LIBRARIES   ###   LIBRARIES
###########################################################################################################################
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal, QThread, QTimer, QEventLoop
import PyQt5.QtCore
import sys
import cv2
import os
from imutils import paths
import face_recognition
import argparse
import pickle
import numpy as np
import time
from train import Train_model
import pickle as dill
import torch
import PIL.Image
from PIL import ImageQt
import torchvision
import torch.nn.functional as F
import torchvision.transforms as transforms
from torch import Tensor
from torch.nn import Linear
from torch.nn import ReLU
from torch.nn import Sigmoid
from torch.nn import Module
from torch.optim import SGD
from torch.nn import BCELoss
from torch.nn.init import kaiming_uniform_
from torch.nn.init import xavier_uniform_
from torch.utils.data import DataLoader
import torch.nn as nn
from torchvision.datasets import CIFAR10
import global_class



from ai import Ai_MainWindow

camera = global_class.camera

"""
###########################################################################################################################
###   OBJECT DETECTION PLAYGROUND CLASS   ###   OBJECT DETECTION PLAYGROUND CLASS   ###   OBJECT DETECTION PLAYGROUND CLASS
###########################################################################################################################
"""
class App(QtWidgets.QMainWindow, Ai_MainWindow):
 def __init__(self, parent):
#  def __init__(self):
   super().__init__()
   self.setupUi(self)
   self.parent = parent
   self.cap = camera
   self.counter = 0
   self.num_files = 115
   self.up.setMaximum(1)
   self.up.setMinimum(0)
   self.down.setMaximum(1)
   self.down.setMinimum(0)
   self.formLayoutWidget.setStyleSheet("background-color: white;"
   "color: black"
   );
   self.timer = QtCore.QTimer()
   self.countLineEdit.setText(str(self.counter))
   self.epochsLineEdit.setText("1")
   self.dataset_values = ["face", "thumbs"]
   self.category_values = {""}
   self.category_array = [["face"], ["thumbs up", "thumbs down"]]
   self.datasetComboBox.addItems(self.dataset_values)
   self.datasetComboBox.setCurrentIndex(-1)
   self.add.clicked.connect(self.save)
   self.stop.clicked.connect(self.stop_live)
   self.train.clicked.connect(self.train_ai)
   self.evaluate.clicked.connect(self.evaluate_ai)
   self.faceNameLineEdit.setEnabled(False)
   self.categoryComboBox.setEnabled(False)


   self.datasetComboBox.activated.connect(self.enable_dataset)
   self.categoryComboBox.activated.connect(self.reset_counter)
   self.transform = transforms.Compose([
       transforms.ColorJitter(0.2,0.2,0.2,0.2),
       transforms.Resize((224,224)),
       transforms.ToTensor(),
       transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
   ])
   self.apply_training = False
   self.is_face = False
   self.is_ai_train = False
   self.cam_is_open = self.cap.isOpened()
   self.start()
 

 """This function stop the timer, close the window and opens the main menu window"""
 def keyPressEvent(self, event):
    key = event.key()
    if key ==  QtCore.Qt.Key_Escape:
    #  self.cap.release()
     self.timer.stop()
     self.close()
     self.parent.showFullScreen()


 """This function stop the ai training by closing all necessary threads and resets necessary values"""
 def stop_live(self):
  if self.is_face:
    self.thread.quit()
    self.thread.wait()
    self.apply_training = False
  else:
   self.data.set_is_on(False)
   self.up.setValue(0)
   self.down.setValue(0)

 """THis function resets the counter"""
 def reset_counter(self):
  self.counter = 0
  self.countLineEdit.setText(str(self.counter))


 """This function create a dataset"""
 def enable_dataset(self):
  self.categoryComboBox.setEnabled(True)
  self.categoryComboBox.clear()
  self.category_values = self.category_array[self.datasetComboBox.currentIndex()]
  self.categoryComboBox.addItems(self.category_values)
  self.reset_counter()
  self.train_model = Train_model("/home/christopher/NSO_LIFE/Practice/Datasets", self.category_values)
  if(self.datasetComboBox.currentText() == "face"):
   self.is_face = True
   self.faceNameLineEdit.setEnabled(True)
  else:
     self.is_face = False
     self.faceNameLineEdit.setEnabled(False)


 """This function defines a pytorch model to be use in training AI """
 def define_models(self):
   #resnet 34
  self.device = torch.device('cpu')
  self.model = torchvision.models.resnet18(pretrained=True)
  self.model.fc = torch.nn.Linear(512, len(self.train_model.dataset.categories ))
  self.model = self.model.to(self.device)
  self.train_dl = DataLoader(self.train_model.dataset, batch_size=1, shuffle=True)
  return (self.train_dl, self.model)

 """This function creates a directory if it doesnt exist """
 def create_if_not_exist(self):
  if not os.path.exists(self.faceNameLineEdit.text()):
    os.makedirs(self.faceNameLineEdit.text())

 """This function starts the timer  which gets the camera frames when expires"""   
 def start(self):
  self.timer.timeout.connect(self.nextFrameSlot)
  self.timer.start(1000./24)

 def start_face_evaluation(self):
  self.face_timer = QtCore.QTimer()
  self.face_timer.timeout.connect(self.getFrameSlot)
  self.face_timer.start(1000./24)


 """This function stops the timer"""
 def stop(self):
  self.timer.stop()

#  def stop_face_eval(self):
#   self.face_timer.stop()
 
 """THis function saved the created pytorch model"""
 def save_model(self):
   torch.save(self.model.state_dict(), "/home/christopher/NSO_LIFE/Practice/my_model.pth")

 """THis function load the created pytorch model"""
 def load_model(self):
  self.model.load_state_dict(torch.load("/home/christopher/NSO_LIFE/Practice/my_model.pth"))


 """This function applies the face training model to find the user and their corresponding faces"""
 def apply_ai_training(self, frame):
  data = pickle.loads(open("/home/christopher/NSO_LIFE/Practice/user_faces.pkl", "rb").read())
  data = np.array(data)
  known_face_encodings = data
  data = pickle.loads(open("/home/christopher/NSO_LIFE/Practice/user_names.pkl", "rb").read())
  known_face_names = data
  face_locations = []
  face_encodings = []
  face_names = []
  process_this_frame = True
  small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
  # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
  rgb_small_frame = small_frame[:, :, ::-1]
  # Only process every other frame of video to save time
  if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.4)
            name = "Unknown"
            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]
            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            counter = 0
            # for i in face_distances:
            #  counter = counter + 1
            #  print("distances at " + str(counter) + ": " + str(i))
            best_match_index = np.argmin(face_distances)
            print(best_match_index)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
            else:
                name = "unknown" #known_face_names[best_match_index]
            face_names.append(name)
        process_this_frame = not process_this_frame
        for (top, right, bottom, left), name in zip(face_locations, face_names):
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
        return frame

 
 def getFrameSlot(self):
     ret, self.frame = self.cap.read()
     self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
     self.save_model()
     self.load_model()
     self.img = PIL.Image.fromarray(self.frame)
    #  self.img = self.process_image(self.img)     
     self.img = self.transform(self.img)
     self.img = self.img.unsqueeze(0)
     output = self.model(self.img)
     output = F.softmax(output, dim=1).detach().numpy().flatten()
    #  output = output.detach().numpy()
     index = output.argmax()
     print("index", index)
     in_val = self.train_model.dataset.categories[index]
     print("predict val ", in_val) 

 """ 
  THis function is responsible for get the camera frames and applying ai trainings to the frames
 """  
 def nextFrameSlot(self):
   if(not self.cam_is_open):
      self.cap = cv2.VideoCapture(0)
      self.cam_is_open = True
   ret, self.frame = self.cap.read()
   self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)

   ##if true apply the face training
   if(self.apply_training and self.is_face):
    self.frame = self.apply_ai_training(self.frame)
    img = QtGui.QImage(self.frame, self.frame.shape[1], self.frame.shape[0], QtGui.QImage.Format_RGB888)
    pix = QtGui.QPixmap.fromImage(img)
    self.image.setPixmap(pix)
   else:
    img = QtGui.QImage(self.frame, self.frame.shape[1], self.frame.shape[0], QtGui.QImage.Format_RGB888)
    pix = QtGui.QPixmap.fromImage(img)
    self.image.setPixmap(pix)
 def test(self, value):
   print("Value ", value) 

 """This function saves capture frames, and save them as images """
 def save(self):
   self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
   if(self.is_face):
    self.create_if_not_exist()
    cv2.imwrite("/home/christopher/NSO_LIFE/Practice/" + self.faceNameLineEdit.text() + "/" + self.countLineEdit.text() + ".jpeg", self.frame)
   else:
     self.train_model.dataset.save_entry(self.frame, self.categoryComboBox.currentText())
   self.counter += 1
   self.countLineEdit.setText(str(self.counter))


 """ This function update the up and down sliders """
 def update_slider(self, index):
      if(index == 0):
           self.up.setValue(1)
           self.down.setValue(0)
      else:
       self.down.setValue(1)
       self.up.setValue(0) 

 """ This function updates the progress bar"""  
 def update_progress(self, value):
   self.progressBar.setValue(value)
  #  if(value == 5):


 """ This function trains the ai by calling the UI THread which take care of that"""
 def train_ai(self):
   self.progressBar.setMaximum(len(self.category_values) * self.counter * int(self.epochsLineEdit.text()))
   self.thread = UI_Thread()
   self.thread.set_is_torch(False)
   self.thread.set_user_directory(self.faceNameLineEdit.text())
   if(not self.is_face):
     self.thread.set_is_torch(True)
     self.train_del, self.model = self.define_models()
     self.thread.set_model(self.model, self.train_dl, int(self.epochsLineEdit.text()))
   self.thread.start()
   self.thread.my_signal.connect(self.update_progress)
 

 """This function evaluate the train datasets by going through the camera frames and check and see if it matches any trained frames"""
 def evaluate_ai(self):
   self.apply_training = True
   if(not self.is_face):
    #  self.stop()
    #  self.start()
     self.save_model()
     self.load_model()
     self.data = DataCaptureThread()
     self.data.set_is_on(True)
     self.data.set(self.transform, self.model, self.train_model)
     self.data.start()
     self.data.my_signal.connect(self.update_slider)
     self.is_ai_train = True
   else:
     self.is_ai_train = False



"""
###########################################################################################################################
###   UI THREAD CLASS   ###   UI THREAD CLASS   ###   UI THREAD CLASS
###########################################################################################################################
"""
class UI_Thread(QThread):
   my_signal = pyqtSignal(int)
   is_torch = False
   model = ""
   train_dl = ""
   user_directory = ""
   epoch = 0


   """
   This function trains the ai by using pytorch adams optimizer. It go through all the images, and the model and train the
   to ai with respect to those images
   """
   def run(self):
    counter = 0
    if(self.is_torch):
      device = torch.device('cpu')
      optimizer = torch.optim.Adam(self.model.parameters())
      self.model = self.model.train()
      criterion = BCELoss()
      # enumerate epochs
      for epoch in range(self.epoch):
        # enumerate mini batches
        sum_loss = 0.0
        error_count = 0.0
        i = 0
        for images, labels in iter(self.train_dl):
            # clear the gradients geget
            images = images.to(device)
            labels = labels.to(device)
            optimizer.zero_grad()
            outputs = self.model(images)
            print(outputs)
            loss = F.cross_entropy(outputs, labels)
            # torch.autograd.set_detect_anomaly(True)
            loss.backward()
            optimizer.step()
            count = len(labels.flatten())
            counter += 1
            error_count += len(torch.nonzero(outputs.argmax(1) - labels).flatten())
            print("error count", error_count)
            i += count
            sum_loss += float(loss)
            accuracy = 1.0 - error_count / i
            # counter = counter / len(self.train_dl)
            print("accuracy ", accuracy)
            self.my_signal.emit(counter)
    else:
     data = []
     names = []
     sPath = "/home/christopher/NSO_LIFE/Practice/" + self.user_directory
     for roots, dirs, files in os.walk(sPath):
      for file in files:
       counter += 1
       print("[INFO] processing image {}/{}".format(counter, len(files)))
       encodings = self.get_encodings(file, sPath)
       if(encodings != ''):
        data.append(encodings)
       file = file[:-1]
       file = file[:-1]
       file = file[:-1]
       file = file[:-1]
       print(file)
       if (encodings != ''):
        names.append(self.user_directory)
       self.my_signal.emit(counter)
     with open('user_faces.pkl', 'ab') as f:
      dill.dump(data, f)
     with open('user_names.pkl', 'ab') as d:
      dill.dump(names, d)
    print("done")
   

   """ THis function sets the user directories """
   def set_user_directory(self, directory):
    self.user_directory = directory
  

   """ This function sets the model """
   def set_model(self, value, train_dl, epoch):
     self.model = value
     self.epoch = epoch
     self.train_dl = train_dl
   ### THis function sets the is_torch boolean
   def set_is_torch(self, value):
     self.is_torch = value
   def get_encodings(self, file, sPath):
    image = face_recognition.load_image_file(sPath + "/" + file)
    encodings = face_recognition.face_encodings(image)
    if len(encodings) > 0:
     encodings = encodings[0]
    else:
     height, width, _ = image.shape
     # location is in css order - top, right, bottom, left
    #  face_location = (0, width, height, 0)
    #  encodings = face_recognition.face_encodings(image, known_face_locations=[face_location])  
     print("No face found")
     return ""
    return encodings

"""
###########################################################################################################################
###   DATA CAPTURED CLASS             ###   DATA CAPTURED CLASS                                ###   DATA CAPTURED CLASS 
###########################################################################################################################
"""
class DataCaptureThread(QThread):
    my_signal = pyqtSignal(int)
    def set_is_on(self, data):
     self.is_on = data
    def set(self, transform, model, train_model):
      self.transform = transform
      self.model = model
      self.train_model = train_model
    """ 
    Evaluate the train model by matching it with the camera frames.
    If the frames are similar it finds the datasets that matches the frames
    """
    def collectProcessData(self):
     if self.is_on:
      self.cap = camera
      ret, self.frame = self.cap.read()
      self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
      self.img = PIL.Image.fromarray(self.frame)
    #  self.img = self.process_image(self.img)     
      self.img = self.transform(self.img)
      self.img = self.img.unsqueeze(0)
      output = self.model(self.img)
      output = F.softmax(output, dim=1).detach().numpy().flatten()
    #  output = output.detach().numpy()
      index = output.argmax() 
      self.my_signal.emit(index)  
      print("index", index)
      in_val = self.train_model.dataset.categories[index]
    #  print("predict val ", in_val) 
     else:
      self.loop.exit()
    def __init__(self, *args, **kwargs):
        QThread.__init__(self, *args, **kwargs)
        self.dataCollectionTimer = QTimer()
        self.dataCollectionTimer.moveToThread(self)
        self.dataCollectionTimer.timeout.connect(self.collectProcessData)

    def run(self):
         self.dataCollectionTimer.start(1000)
         self.loop = QEventLoop()
         self.loop.exec_()

# if __name__ == '__main__':
#   app = QApplication(sys.argv)
#   form = App()
#   form.show()
#   app.exec_()