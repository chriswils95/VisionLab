from playground import ComputerVisionPlayground
from main import Ui_MainWindow
from ai import Ai_MainWindow
from app import App
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget
from PyQt5.QtGui import QPalette, QBrush, QPixmap, QMovie
from PyQt5.QtCore import pyqtSignal, QThread, QTimer, QEventLoop
from PyQt5.QtCore import Qt
import PyQt5.QtCore
import threading
from PyQt5.Qt import QImage, Qt
import sys
import cv2
import os
import tkinter as tk
import global_class 
from PyQt5.QtGui import QPixmap, QPainter
from Basic_stylesheet import main_stylesheet
from similarity import Similarity_window


"""
###########################################################################################################################
###   PLAYGROUND WINDOW CLASS   ###   PLAYGROUND WINDOW CLASS   ###   PLAYGROUND WINDOW CLASS
###########################################################################################################################
"""
class Second_Window():
  """This function opens the playground window and close the main window"""
  def __init__(self, parent):
   self.parent = parent
   self.playground_window = ComputerVisionPlayground()
   self.playground_window.master.bind("<Escape>", self.keyPressEvent)
   self.playground_window.master.mainloop()


  """This function exit out this window and open the main window"""
  def keyPressEvent(self, event):
    self.playground_window.master.destroy()
    self.parent.showFullScreen()
    
     

"""
###########################################################################################################################
###   MAIN WINDOW CLASS   ###   MAIN WINDOW CLASS   ###   MAIN WINDOW CLASS
###########################################################################################################################
"""
class Window(QtWidgets.QMainWindow, Ui_MainWindow):
  """This function opens the main window and lsitens for window frames click"""
  def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.playground.mousePressEvent = self.show_playground
        self.train.mousePressEvent = self.show_ai_playground
        self.church.mousePressEvent = self.show_celebrity_playground

  
  """This function opens the similarity face window"""
  def show_celebrity_playground(self, event):
   self.similarity_win = Similarity_window(self)
   self.similarity_win.showFullScreen()

  """THis function opens the playground window"""
  def show_playground(self, event):
   self.playground_window = Second_Window(self)


  """This function opens the object detection window """
  def show_ai_playground(self, event):
     self.app = App(self)
     self.app.showFullScreen()


  """
  This is an internal pyqt fucntion that is override to detect key presses
  In this case we override it to close the mainwindow on escape key pressed
  """
  def keyPressEvent(self, event):
    key = event.key()
    if key == Qt.Key_Escape:
        global_class.camera.release()
        self.close()

if __name__ == '__main__':
  

  app = QApplication(sys.argv)
  form = Window()
  form.showFullScreen()
  app.setStyleSheet(main_stylesheet)
  app.exec_()
 
