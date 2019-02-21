import sys
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow
from PyQt5.QtGui import QPixmap, QImage                                
from PyQt5.QtCore import *
from PyQt5 import QtWidgets
from passcode import Ui_Dialog
from home_screen import HomeScreen
import cv2


### this is gun comment ###
passcodes = ''
class Thread(QThread):
    changePixmap = pyqtSignal(QImage)
    def run(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if ret:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                #p = QPixmap.fromImage(rgbImage)    
                #p = p.scaled(640, 480, Qt.KeepAspectRatio)
                convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QImage.Format_RGB888)
                p = convertToQtFormat.scaled(320, 240, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)
class HomeApp(QMainWindow):
    @pyqtSlot(QImage)
    def setImage(self, image):
        self.ui.label.setPixmap(QPixmap.fromImage(image))
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = HomeScreen()
        self.ui.setupHomeScreen(self)
        th = Thread(self)
        th.changePixmap.connect(self.setImage)
        th.start()
class MyApp(QMainWindow):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
    def printTest(self):
        print('clicked !!!!!')
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
        self.ui.password_field.repaint()
    def checkPassword(self):
        global passcodes
        if(len(passcodes) >= 4):
            if(passcodes == '1234'):
                print('Correct')
                #self.hide()
                homeapp = HomeApp(self)
                homeapp.show()
            else:
                print('Wrong')
                passcodes = ''
                self.printPasscode() 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    myapp = MyApp()
    myapp.show()
    sys.exit(app.exec_())
