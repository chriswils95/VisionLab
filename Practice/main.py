# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'basicwindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MenuWindow")
        MainWindow.resize(1280, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.playground = QtWidgets.QFrame(self.centralwidget)
        self.playground.setGeometry(QtCore.QRect(800, 180, 341, 291))
        self.playground.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.playground.setFrameShadow(QtWidgets.QFrame.Raised)
        self.playground.setObjectName("playground")
        self.church = QtWidgets.QFrame(self.centralwidget)
        self.church.setGeometry(QtCore.QRect(350, 620, 341, 291))
        self.church.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.church.setFrameShadow(QtWidgets.QFrame.Raised)
        self.church.setObjectName("church")
        self.train = QtWidgets.QFrame(self.centralwidget)
        self.train.setGeometry(QtCore.QRect(1190, 620, 341, 291))
        self.train.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.train.setFrameShadow(QtWidgets.QFrame.Raised)
        self.train.setObjectName("train")
        self.header = QtWidgets.QLabel(self.centralwidget)
        self.header.setGeometry(QtCore.QRect(0, 0, 2000, 100))
        self.header.setObjectName("header")
        self.train_lb = QtWidgets.QLabel(self.centralwidget)
        self.train_lb.setGeometry(QtCore.QRect(1040, 580, 600, 30))
        self.train_lb.setObjectName("train_lb")
        self.church_lb = QtWidgets.QLabel(self.centralwidget)
        self.church_lb.setGeometry(QtCore.QRect(220, 580, 600, 30))
        self.church_lb.setObjectName("church_lb")
        self.playground_lb = QtWidgets.QLabel(self.centralwidget)
        self.playground_lb.setGeometry(QtCore.QRect(600, 140, 600, 50))
        self.playground_lb.setObjectName("playground_lb")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1280, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.header.setText(_translate("MainWindow", "BRIGHAM YOUNG UNIVERSITY VISION PROJECT"))
        self.train_lb.setText(_translate("MainWindow", "Object Detection"))
        self.church_lb.setText(_translate("MainWindow", "Similarity Face Detection"))
        self.playground_lb.setText(_translate("MainWindow", "                     Computer Vision Playground"))

