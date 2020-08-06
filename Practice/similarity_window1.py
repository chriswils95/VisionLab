# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'similaritywindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1051, 642)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(100, 120, 600, 471))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.train_label = QtWidgets.QLabel(self.frame)
        self.train_label.setGeometry(QtCore.QRect(0, 0, 600, 471))
        self.train_label.setText("")
        self.train_label.setPixmap(QtGui.QPixmap("../../Downloads/test.jpg"))
        self.train_label.setObjectName("train_label")
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(1200, 120, 600, 471))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.live_label = QtWidgets.QLabel(self.frame_2)
        self.live_label.setGeometry(QtCore.QRect(0, 0, 600, 471))
        self.live_label.setText("")
        self.live_label.setPixmap(QtGui.QPixmap("../../Downloads/test.jpg"))
        self.live_label.setObjectName("live_label")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 2000, 100))
        self.label.setObjectName("header")
        self.frame_3 = QtWidgets.QFrame(self.centralwidget)
        self.frame_3.setGeometry(QtCore.QRect(0, 100, 2000, 1000))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.stop = QtWidgets.QPushButton(self.frame_3)
        self.stop.setGeometry(QtCore.QRect(850, 800, 89, 50))
        self.stop.setText("STOP")
        self.stop.setObjectName("stop")
        self.start = QtWidgets.QPushButton(self.frame_3)
        self.start.setGeometry(QtCore.QRect(950, 800, 89, 50))
        self.start.setText("START")
        self.start.setObjectName("start")
        self.reset = QtWidgets.QPushButton(self.frame_3)
        self.reset.setGeometry(QtCore.QRect(1050, 800, 89, 50))
        self.reset.setText("RESET")
        self.reset.setObjectName("reset")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1051, 22))
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
        self.label.setText(_translate("MainWindow", "Similarity Face Detection"))

