# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'signinscreen.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SignIn(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(800, 480)
        Dialog.setAutoFillBackground(True)
        Dialog.setStyleSheet("background-color:#00334e;")
        #Dialog.setStyleSheet("background-image: url(images/sky.jpg);")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setStyleSheet("color:#FFFFFF;")
        self.label.setGeometry(QtCore.QRect(75, 40, 690, 71))
        font = QtGui.QFont()
        font.setPointSize(28)
        self.label.setFont(font)
        self.label.setObjectName("label")
        font.setPointSize(13)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setStyleSheet("color:#FFFFFF;")
        self.label_2.setFont(font)
        self.label_2.setGeometry(QtCore.QRect(220, 135, 350, 380))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setStyleSheet("color:#FFFFFF;")
        self.label_3.setGeometry(QtCore.QRect(260, 110, 330, 61))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setStyleSheet("color:#000000;")
        self.pushButton.setGeometry(QtCore.QRect(600, 390, 160, 70))

        self.pushButton2 = QtWidgets.QPushButton(Dialog)
        self.pushButton2.setStyleSheet("color:#000000;")
        self.pushButton2.setGeometry(QtCore.QRect(600, 390, 160, 70))

        font = QtGui.QFont()
        font.setPointSize(20)
        self.pushButton.setFont(font)
        
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Welcome To Home Automation System"))
        self.label_2.setText(_translate("Dialog", "TextLabel"))
        self.label_3.setText(_translate("Dialog", "Please scan QRcode for Sign in"))
        self.pushButton.setText(_translate("Dialog", "Take Photos."))
        self.pushButton2.setText(_translate("Dialog", "Start"))
