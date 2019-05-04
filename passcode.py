# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'passcode.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from functools import partial


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(800, 480)
        Dialog.setStyleSheet("background-color:#00334e;")
        self.x = 200
        self.offset = self.x-50
        font = QtGui.QFont()
        font.setPointSize(16) 

        self.btn_finger = QtWidgets.QPushButton(Dialog)
        self.btn_finger.setFont(font)
        self.btn_finger.setStyleSheet("color:#000000;")
        self.btn_finger.setGeometry(QtCore.QRect(80, 320, 160, 60))
        self.btn_finger.setObjectName("btn_finger")

        self.btn_photo = QtWidgets.QPushButton(Dialog)
        self.btn_photo.setFont(font)
        self.btn_photo.setStyleSheet("color:#000000;")
        self.btn_photo.setGeometry(QtCore.QRect(80, 250, 160, 60))
        self.btn_photo.setObjectName("btn_photo")
        self.btn_photo.setEnabled(False)

        self.label_beacon = QtWidgets.QLabel(Dialog)
        self.label_beacon.setGeometry(QtCore.QRect(80, 390, 200, 30))
        font.setPointSize(18)
        self.label_beacon.setFont(font)
        self.label_beacon.setStyleSheet('color:#FFFFFF;') 
        self.label_beacon.setAlignment(QtCore.Qt.AlignCenter)
        self.label_beacon.setObjectName("label_beacon")

        font.setPointSize(35)
        self.btn_1 = QtWidgets.QPushButton(Dialog)
        self.btn_1.setFont(font)
        self.btn_1.setStyleSheet('color:#000000;') 
        #self.btn_1.setStyleSheet("color:#e8e8e8;")
        self.btn_1.setGeometry(QtCore.QRect(160+self.x, 110, 100, 90))
        self.btn_1.setObjectName("btn_1")

        self.btn_2 = QtWidgets.QPushButton(Dialog)
        self.btn_2.setFont(font)
        self.btn_2.setStyleSheet('color:#000000;') 
        self.btn_2.setGeometry(QtCore.QRect((350)+self.offset, 110, 100, 90))
        self.btn_2.setObjectName("btn_2")

        self.btn_3 = QtWidgets.QPushButton(Dialog)
        self.btn_3.setFont(font)
        self.btn_3.setStyleSheet('color:#000000;') 
        self.btn_3.setGeometry(QtCore.QRect((490)+self.offset, 110, 100, 90))
        self.btn_3.setObjectName("btn_3")

        self.btn_4 = QtWidgets.QPushButton(Dialog)
        self.btn_4.setFont(font)
        self.btn_4.setStyleSheet('color:#000000;') 
        self.btn_4.setGeometry(QtCore.QRect(160+self.x, 200, 100, 90))
        self.btn_4.setObjectName("btn_4")

        self.btn_5 = QtWidgets.QPushButton(Dialog)
        self.btn_5.setFont(font)
        self.btn_5.setStyleSheet('color:#000000;') 
        self.btn_5.setGeometry(QtCore.QRect(350+self.offset, 200, 100, 90))
        self.btn_5.setObjectName("btn_5")

        self.btn_6 = QtWidgets.QPushButton(Dialog)
        self.btn_6.setFont(font)
        self.btn_6.setStyleSheet('color:#000000;') 
        self.btn_6.setGeometry(QtCore.QRect(490+self.offset, 200, 100, 90))
        self.btn_6.setObjectName("btn_6")

        self.btn_7 = QtWidgets.QPushButton(Dialog)
        self.btn_7.setFont(font)
        self.btn_7.setStyleSheet('color:#000000;') 
        self.btn_7.setGeometry(QtCore.QRect(160+self.x, 290, 100, 90))
        self.btn_7.setObjectName("btn_7")

        self.btn_8 = QtWidgets.QPushButton(Dialog)
        self.btn_8.setFont(font)
        self.btn_8.setStyleSheet('color:#000000;') 
        self.btn_8.setGeometry(QtCore.QRect(350+self.offset, 290, 100, 90))
        self.btn_8.setObjectName("btn_8")

        self.btn_9 = QtWidgets.QPushButton(Dialog)
        self.btn_9.setFont(font)
        self.btn_9.setStyleSheet('color:#000000;') 
        self.btn_9.setGeometry(QtCore.QRect(490+self.offset, 290, 100, 90))
        self.btn_9.setObjectName("btn_9")

        self.btn_0 = QtWidgets.QPushButton(Dialog)
        self.btn_0.setFont(font)
        self.btn_0.setStyleSheet('color:#000000;') 
        self.btn_0.setGeometry(QtCore.QRect(350+self.offset, 380, 100, 90))
        self.btn_0.setObjectName("btn_0")

        self.btn_del = QtWidgets.QPushButton(Dialog)
        self.btn_del.setFont(font)
        self.btn_del.setStyleSheet('color:#000000;') 
        self.btn_del.setGeometry(QtCore.QRect(490+self.offset, 380, 100, 90))
        self.btn_del.setObjectName("btn_del")
        
        self.password_field = QtWidgets.QLabel(Dialog)
        self.password_field.setStyleSheet('color:#FFFFFF;') 
        self.password_field.setGeometry(QtCore.QRect(230+self.x, 50, 240, 50))
        self.password_field.setFrameShape(QtWidgets.QFrame.StyledPanel)

        font.setPointSize(50)
        font.setBold(True)

        self.password_field.setFont(font)
        self.password_field.setText("")
        self.password_field.setAlignment(QtCore.Qt.AlignCenter)
        self.password_field.setObjectName("password_field")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(230+self.x, 10, 250, 30))
        font.setPointSize(20)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label_2.setStyleSheet('color:#FFFFFF;')
        #####
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(40, 5, 256, 256))
        font.setPointSize(18)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")

        self.retranslateUi(Dialog)
        ####################
        self.btn_1.clicked.connect(partial(Dialog.enterCode, '1'))
        self.btn_2.clicked.connect(partial(Dialog.enterCode, '2'))
        self.btn_3.clicked.connect(partial(Dialog.enterCode, '3'))
        self.btn_4.clicked.connect(partial(Dialog.enterCode, '4'))
        self.btn_5.clicked.connect(partial(Dialog.enterCode, '5'))
        self.btn_6.clicked.connect(partial(Dialog.enterCode, '6'))
        self.btn_7.clicked.connect(partial(Dialog.enterCode, '7'))
        self.btn_8.clicked.connect(partial(Dialog.enterCode, '8'))
        self.btn_9.clicked.connect(partial(Dialog.enterCode, '9'))
        self.btn_0.clicked.connect(partial(Dialog.enterCode, '0'))
        self.btn_finger.clicked.connect(partial(Dialog.fingerScan, 1))
        self.btn_photo.clicked.connect(partial(Dialog.takePhoto))
        self.btn_del.clicked.connect(Dialog.enterDelete)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.btn_1.setText(_translate("Dialog", "1"))
        self.btn_2.setText(_translate("Dialog", "2"))
        self.btn_3.setText(_translate("Dialog", "3"))
        self.btn_4.setText(_translate("Dialog", "4"))
        self.btn_5.setText(_translate("Dialog", "5"))
        self.btn_6.setText(_translate("Dialog", "6"))
        self.btn_7.setText(_translate("Dialog", "7"))
        self.btn_8.setText(_translate("Dialog", "8"))
        self.btn_9.setText(_translate("Dialog", "9"))
        self.btn_0.setText(_translate("Dialog", "0"))
        self.btn_del.setText(_translate("Dialog", "<"))
        self.label_2.setText(_translate("Dialog", "Enter Passcode"))
        self.label_3.setText(_translate("Dialog", "555+++"))
        self.label_beacon.setText(_translate("Dialog", "Beacon status:..."))
        self.btn_finger.setText(_translate("Dialog", "fingerprint scan"))
        self.btn_photo.setText(_translate("Dialog", "Hold and still.."))

