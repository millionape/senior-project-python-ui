import sys
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow
from PyQt5 import QtWidgets
from passcode import Ui_Dialog
from home_screen import HomeScreen

passcodes = ''

class MyApp(QMainWindow):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.btn_1.clicked.connect(lambda: self.enterCode('1'))
        self.ui.btn_2.clicked.connect(lambda: self.enterCode('2'))
        self.ui.btn_3.clicked.connect(lambda: self.enterCode('3'))
        self.ui.btn_4.clicked.connect(lambda: self.enterCode('4'))
        self.ui.btn_5.clicked.connect(lambda: self.enterCode('5'))
        self.ui.btn_6.clicked.connect(lambda: self.enterCode('6'))
        self.ui.btn_7.clicked.connect(lambda: self.enterCode('7'))
        self.ui.btn_8.clicked.connect(lambda: self.enterCode('8'))
        self.ui.btn_9.clicked.connect(lambda: self.enterCode('9'))
        self.ui.btn_0.clicked.connect(lambda: self.enterCode('0'))
        self.ui.btn_del.clicked.connect(self.enterDelete)

    def enterCode(self, n) :
        global passcodes
        passcodes += n
        self.printPasscode()
        self.checkPassword()
    def enterDelete(self) :
        global passcodes
        passcodes = ''
        self.printPasscode()
    def printPasscode(self):
        global passcodes
        n = len(passcodes)
        text = ''
        for i in range(n):
            text += '*'
        self.ui.password_field.setText(text)
    def checkPassword(self):
        global passcodes
        if(len(passcodes) >= 4):
            if(passcodes == '1234'):
                print('Correct')
                self.hide()
                self.homeScreens = QtWidgets.QMainWindow()
                self.ui = HomeScreen()
                self.ui.setupHomeScreen(self.homeScreens)
                self.homeScreens.show()
            else:
                print('Wrong')
                passcodes = ''
                self.printPasscode()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myapp = MyApp()
    myapp.show()
    sys.exit(app.exec_())
