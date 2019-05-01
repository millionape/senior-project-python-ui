# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'home.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class HomeScreen(object):
    def setupHomeScreen(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(800, 480)
        Dialog.setStyleSheet("background-color:#7391A6;")
        self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget.setStyleSheet("background-color:#1B4F6C;")
        self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 20, 500, 400))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        ####
        # self.pushButton_2 = QtWidgets.QPushButton(self.gridLayoutWidget)
        # self.pushButton_2.setObjectName("pushButton_2")
        # self.pushButton_2.setFixedSize( 100, 100 )
        # self.gridLayout.addWidget(self.pushButton_2, 1, 0, 1, 1)
        # self.pushButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        # self.pushButton.setObjectName("pushButton")
        # self.pushButton.setFixedSize( 100, 100 )
        # self.gridLayout.addWidget(self.pushButton, 0, 0, 1, 1)
        # self.pushButton_3 = QtWidgets.QPushButton(self.gridLayoutWidget)
        # self.pushButton_3.setObjectName("pushButton_3")
        # self.pushButton_3.setFixedSize( 100, 100 )
        # self.gridLayout.addWidget(self.pushButton_3, 0, 1, 1, 1)
        
        # self.pushButton_4 = QtWidgets.QPushButton(self.gridLayoutWidget)
        # self.pushButton_4.setObjectName("pushButton_4")
        # self.gridLayout.addWidget(self.pushButton_4, 1, 1, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        # self.pushButton_2.setText(_translate("Dialog", "PushButton"))
        # self.pushButton.setText(_translate("Dialog", "PushButton"))
        # self.pushButton_3.setText(_translate("Dialog", "PushButton"))
        #self.pushButton_4.setText(_translate("Dialog", "PushButton"))


