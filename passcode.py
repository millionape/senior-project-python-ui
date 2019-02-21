# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'passcode.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(834, 601)
        self.btn_1 = QtWidgets.QPushButton(Dialog)
        self.btn_1.setGeometry(QtCore.QRect(160, 160, 100, 90))
        self.btn_1.setObjectName("btn_1")
        self.btn_2 = QtWidgets.QPushButton(Dialog)
        self.btn_2.setGeometry(QtCore.QRect(350, 160, 100, 90))
        self.btn_2.setObjectName("btn_2")
        self.btn_3 = QtWidgets.QPushButton(Dialog)
        self.btn_3.setGeometry(QtCore.QRect(540, 160, 100, 90))
        self.btn_3.setObjectName("btn_3")
        self.btn_4 = QtWidgets.QPushButton(Dialog)
        self.btn_4.setGeometry(QtCore.QRect(160, 260, 100, 90))
        self.btn_4.setObjectName("btn_4")
        self.btn_5 = QtWidgets.QPushButton(Dialog)
        self.btn_5.setGeometry(QtCore.QRect(350, 260, 100, 90))
        self.btn_5.setObjectName("btn_5")
        self.btn_6 = QtWidgets.QPushButton(Dialog)
        self.btn_6.setGeometry(QtCore.QRect(540, 260, 100, 90))
        self.btn_6.setObjectName("btn_6")
        self.btn_7 = QtWidgets.QPushButton(Dialog)
        self.btn_7.setGeometry(QtCore.QRect(160, 360, 100, 90))
        self.btn_7.setObjectName("btn_7")
        self.btn_8 = QtWidgets.QPushButton(Dialog)
        self.btn_8.setGeometry(QtCore.QRect(350, 360, 100, 90))
        self.btn_8.setObjectName("btn_8")
        self.btn_9 = QtWidgets.QPushButton(Dialog)
        self.btn_9.setGeometry(QtCore.QRect(540, 360, 100, 90))
        self.btn_9.setObjectName("btn_9")
        self.btn_0 = QtWidgets.QPushButton(Dialog)
        self.btn_0.setGeometry(QtCore.QRect(350, 460, 100, 90))
        self.btn_0.setObjectName("btn_0")
        self.btn_del = QtWidgets.QPushButton(Dialog)
        self.btn_del.setGeometry(QtCore.QRect(540, 460, 100, 90))
        self.btn_del.setObjectName("btn_del")
        self.password_field = QtWidgets.QLabel(Dialog)
        self.password_field.setGeometry(QtCore.QRect(280, 80, 240, 50))
        self.password_field.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.password_field.setText("")
        self.password_field.setAlignment(QtCore.Qt.AlignCenter)
        self.password_field.setObjectName("password_field")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(300, 40, 200, 30))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Dialog)
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


