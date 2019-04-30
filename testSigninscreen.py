from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow ,QMessageBox
from functools import partial
from PyQt5.QtGui import QPixmap, QImage                                
from PyQt5.QtCore import *
from PyQt5 import QtWidgets
import threading
from signinscreen import Ui_SignIn
import cv2
import numpy as np
import sys
from pyzbar import pyzbar
import json 

class ThreadQR(QThread):
    changePixmap = pyqtSignal(QImage)
    state = pyqtSignal()
    take = pyqtSignal(np.ndarray)
    imgSave = None
    flag = True
    #cap = cv2.VideoCapture(0)
    def run(self):
        self.cap = cv2.VideoCapture(0)
        while self.cap.isOpened() and self.flag:
            ret, frame = self.cap.read()
            if ret:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                barcodes = pyzbar.decode(rgbImage)
                for barcode in barcodes:
                    (x, y, w, h) = barcode.rect
                    cv2.rectangle(rgbImage, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    barcodeData = barcode.data.decode("utf-8")
                    barcodeType = barcode.type
                    text = "{} ({})".format(barcodeData, barcodeType)  
                    try:
                        b = json.loads(barcodeData)
                        if b['type'] == 'login':
                            print(b['user'],b['password'])  
                            cv2.putText(rgbImage,b['user'], (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                                5, (0, 0, 255), 2)  
                            self.blank_image = np.zeros((350,350,3), np.uint8)
                            self.cap.release()  
                            # self.state.emit()
                            self.stop()
                        else:
                            cv2.putText(rgbImage,"QR code is not correct", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                                5, (0, 0, 255), 2)  
                    except:
                        cv2.putText(rgbImage,"Format error", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                            5, (0, 0, 255), 2)  

                    
                    
                    
                
                    # print the barcode type and data to the terminal
                    print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))
                #p = QPixmap.fromImage(rgbImage)    
                #p = p.scaled(640, 480, Qt.KeepAspectRatio)
                convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QImage.Format_RGB888)
                p = convertToQtFormat.scaled(350, 220)
                self.imgSave = rgbImage
                self.changePixmap.emit(p)
    def __del__(self):
        self.flag = False
        self.quit()
        self.wait()
    def take_photo(self):
            self.take.emit(self.imgSave)
    def stop(self):
            self.flag = False
            #self.quit()
            self.cap.release()
            self.state.emit()
            #self.quit()
            #self.terminate()

class MyAppSignIn(QMainWindow):
    img1 = None
    @pyqtSlot(QImage)
    def setImage(self, image):
        #self.img1 = QPixmap.fromImage(image)
        self.ui.label_2.setPixmap(QPixmap.fromImage(image))
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = Ui_SignIn()
        self.ui.setupUi(self)
        self.blank_image = np.zeros((350,350,3), np.uint8)
        #self.blank_image[:,0:256//2] = (224,224,224)      # (B, G, R)
        #self.blank_image[:,256//2:256] = (0,0,0)
        cv2.putText(self.blank_image,"Welcome", (40,50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255,255,255))
        self.convertToQtFormat = QImage(self.blank_image.data, self.blank_image.shape[1], self.blank_image.shape[0], QImage.Format_RGB888)
        self.ui.label_2.setPixmap(QPixmap.fromImage(self.convertToQtFormat))
        th = ThreadQR(self)
        th.changePixmap.connect(self.setImage)
        th.start()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myapp = MyAppSignIn()
    myapp.show()
    sys.exit(app.exec_())