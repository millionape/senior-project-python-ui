#!/usr/bin/python3
import sys
import blescan3
import bluetooth._bluetooth as bluez
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow ,QMessageBox
from functools import partial
from PyQt5.QtGui import QPixmap, QImage  ,QFont                              
from PyQt5.QtCore import *
from PyQt5 import QtWidgets
from passcode import Ui_Dialog
from home import HomeScreen
import cv2
import hashlib
from pyfingerprint.pyfingerprint import PyFingerprint
import numpy as np
import hashlib

import math
from sklearn import neighbors
import os
import os.path
import pickle
from PIL import Image, ImageDraw
import face_recognition
from face_recognition.face_recognition_cli import image_files_in_folder
from pyrebase import pyrebase
import json
import serial
import threading
import time

from pyzbar import pyzbar
from signinscreen import Ui_SignIn
USB_FINGER_PORT = '/dev/ttyUSB1'
#USB_FINGER_PORT = '/dev/tty.usbserial'
authEmail = ""
authPass = ""
#port = '/dev/tty.usbserial-1410'
port = '/dev/ttyUSB0'
baud = 115200
ser = serial.Serial(port, baud)
delayTime = 0.6
config = {
    "apiKey": "AIzaSyBL8AZt1Oq2B1EuDOQ-su43SobhObUFdBc",
    "authDomain": "final-project-80b54.firebaseapp.com",
    "databaseURL": "https://final-project-80b54.firebaseio.com",
    "storageBucket": "final-project-80b54.appspot.com",
    "serviceAccount": "final-project-80b54-firebase-adminsdk-wm3vj-5a8bc8ff20.json"
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
uid = ""
db = firebase.database()
buttonDict = {}
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
passAuth = False
faceAuth = False
fingerAuth = False
bleAuth = False
### this is gun comment ###
passcodes = ''
serRead = True
class ThreadQR(QThread):
    changePixmap = pyqtSignal(QImage)
    state = pyqtSignal(int)
    take = pyqtSignal(np.ndarray)
    imgSave = None
    flag = True
    def run(self):
        global uid
        global auth
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
                            try:
                                user = auth.sign_in_with_email_and_password(b['user'], b['password'])
                                    # before the 1 hour expiry:
                                user = auth.refresh(user['refreshToken'])
                                    # now we have a fresh token
                                uid = user['userId']
                                print("this is uid from thread :{}".format(uid))
                                with open('auth.json', 'w') as outfile:  
                                    json.dump(b, outfile)
                                self.state.emit(1)
                                self.stop()
                                self.cap.release() 
                            except:
                                # Auth failue
                                print('some error : auth fail')
                                self.state.emit(0)                       
                        else:
                            cv2.putText(rgbImage,"QR code is not correct", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                                5, (0, 0, 255), 2)  
                    except:
                        pass
                    print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))
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
            self.cap.release()
class ThreadFace(QThread):
    changePixmap = pyqtSignal(QImage)
    stateFace = pyqtSignal(int)
    take = pyqtSignal(np.ndarray)
    imgSave = None
    flag = True
    takeFlag = False
    count = 0
    def run(self):
        global uid
        global auth
        self.cap = cv2.VideoCapture(0)
        while self.cap.isOpened() and self.flag:
            ret, frame = self.cap.read()
            if ret:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                if self.takeFlag and self.count<30:
                    self.count += 1
                    cv2.putText(rgbImage,"Taking Photos :{}".format(self.count), (0,120), cv2.FONT_HERSHEY_SIMPLEX,3, (0, 0, 255), 2) 
                    cv2.imwrite('facesImage/0{}.png'.format(self.count),rgbImage)
                if self.count >= 30:
                    self.flag = False
                    self.stateFace.emit(1)
                    self.cap.release() 
                    self.quit()
                convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QImage.Format_RGB888)
                p = convertToQtFormat.scaled(350, 220)
                self.imgSave = rgbImage
                self.changePixmap.emit(p)
    def __del__(self):
        self.flag = False
        self.quit()
        self.wait()
    def take_photo(self):
        self.takeFlag = True
        #self.take.emit(self.imgSave)
    def stop(self):
        self.flag = False
        self.cap.release()
        self.quit()
class ThreadFinger(QThread):
    changePixmap = pyqtSignal(QImage)
    stateFinger = pyqtSignal(int)
    take = pyqtSignal(np.ndarray)
    imgSave = None
    flag = True
    takeFlag = False
    count = 0
    def run(self):
        try:
            f = PyFingerprint(USB_FINGER_PORT, 57600, 0xFFFFFFFF, 0x00000000)
            if ( f.verifyPassword() == False ):
                raise ValueError('The given fingerprint sensor password is wrong!')
        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Error")
            msg.setInformativeText("fingerprint sensor could not be initialized!")
            msg.setWindowTitle("Error.")
            msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_()
            if retval == QMessageBox.Ok:
                print('The fingerprint sensor could not be initialized!')
                print('Exception message: ' + str(e))
                exit(1)
        print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))
        if f.getTemplateCount() > 0:
            try:
                for i in range(f.getTemplateCount()):
                    if ( f.deleteTemplate(i) == True ):
                        print('Template deleted!')

            except Exception as e:
                print('Operation failed!')
                print('Exception message: ' + str(e))
                exit(1)
        try:
            self.stateFinger.emit(1)
            print('Waiting for finger...')
            while ( f.readImage() == False ):
                pass
            f.convertImage(0x01)
            result = f.searchTemplate()
            positionNumber = result[0]
            if ( positionNumber >= 0 ):
                # self.ui.label_2.setText('This finger already exists at position #' + str(positionNumber))
                print('Template already exists at position #' + str(positionNumber))
                exit(0)
            self.stateFinger.emit(2)
            #self.ui.label_2.setText("Step 2: Remove your finger from the sensor.")
            print('Remove finger...')
            time.sleep(2)
            self.stateFinger.emit(3)
            #self.ui.label_2.setText("Step 3: Put your finger on the sensor again.")
            print('Waiting for same finger again...')
            while ( f.readImage() == False ):
                time.sleep(0.2)
                pass
            f.convertImage(0x02)
            if ( f.compareCharacteristics() == 0 ):
                raise Exception('Fingers do not match')
                self.stateFinger.emit(5)
            f.createTemplate()
            positionNumber = f.storeTemplate()
            # self.ui.label_2.setText("Finger enrolled successfully!")
            print('Finger enrolled successfully!')
            print('New template position #' + str(positionNumber))
            self.stateFinger.emit(4)
        except Exception as e:
            print('Operation failed!')
            print('Exception message: ' + str(e))
            exit(1)

    def __del__(self):
        self.flag = False
        self.quit()
        self.wait()
    def take_photo(self):
        self.takeFlag = True
        #self.take.emit(self.imgSave)
    def stop(self):
        self.flag = False
        self.cap.release()
class MyAppSignIn(QMainWindow):
    img1 = None
    @pyqtSlot(QImage)
    def setImage(self, image):
        self.ui.label_2.setPixmap(QPixmap.fromImage(image))
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = Ui_SignIn()
        self.ui.setupUi(self)
        self.ui.pushButton.hide()
        self.ui.pushButton2.hide()
        self.ui.pushButton2.clicked.connect(self.enrollFinger)
        self.blank_image = np.zeros((350,350,3), np.uint8)
        cv2.putText(self.blank_image,"Welcome", (40,50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255,255,255))
        self.convertToQtFormat = QImage(self.blank_image.data, self.blank_image.shape[1], self.blank_image.shape[0], QImage.Format_RGB888)
        self.ui.label_2.setPixmap(QPixmap.fromImage(self.convertToQtFormat))
        self.thf = ThreadFace(self)
        self.thf.changePixmap.connect(self.setImage)
        self.thf.stateFace.connect(self.faceCapture)

        self.thFinger = ThreadFinger(self)
        self.thFinger.stateFinger.connect(self.showLabel)

        self.ui.pushButton.clicked.connect(self.thf.take_photo)
        self.th = ThreadQR(self)
        self.th.changePixmap.connect(self.setImage)
        self.th.state.connect(self.authPass)
        self.th.start()

    def enrollFinger(self):
        self.thFinger.start()
    def showLabel(self,x):
        if x==1:
            self.ui.label_2.setText("Step 1: Put your finger on the sensor.")
        elif x==2:
            self.ui.label_2.setText("Step 2: Remove your finger from the sensor.")
        elif x==3:
            self.ui.label_2.setText("Step 3: Put your finger on the sensor again.")
        elif x==4:
            self.ui.label_2.setText("Success enroll new finger.")
            app = PasswordSettingApp()
            app.showFullScreen() 
            # myappDash = MyApp()
            # myappDash.show()
            self.close()
        elif x==5:
            self.ui.label_2.setText("Error finger doesn't match , Please start again.")
            self.thFinger.stop()

         


            

    def faceCapture(self,x):
        print("Face capture success")
        self.thf.stop()
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Success")
        msg.setInformativeText("Next please enroll your fingerprint.")
        msg.setWindowTitle("Success.")
        msg.setStandardButtons(QMessageBox.Ok)
        retval = msg.exec_()
        if retval == QMessageBox.Ok:
            print("okkkk")
            self.ui.label_3.setText("")
            self.ui.label_2.setText("Tap on start button for enroll your new finger.")
            self.ui.pushButton.hide()
            self.ui.pushButton2.show() 
            # myappDash = MyApp()
            # myappDash.show()
            # self.close()
            
    def msgbtn(self,i):
        print ("Button pressed is:",i.text())
        self.th = ThreadQR(self)
        self.th.changePixmap.connect(self.setImage)
        self.th.state.connect(self.authPass)
        self.th.start()
    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Escape:
            print('esc')
            self.th.stop()
            self.close()
    def authPass(self,x):
        if x == 1:
            print('auth pass')
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)

            msg.setText("Authentication Success.")
            msg.setInformativeText("Next please taking your face photos.")
            msg.setWindowTitle("Success.")
            msg.setStandardButtons(QMessageBox.Ok)
            #msg.buttonClicked.connect(self.msgbtn)
            retval = msg.exec_()
            if retval == QMessageBox.Ok:
                self.ui.pushButton.show()
                self.ui.label_3.setText("Please tap on \"TakePhotos\" button down below.")
                self.thf.start()
            
            # myappDash = MyApp()
            # myappDash.show()
            #self.close()
        else:
            self.th.stop()
            print("auth not pass")
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)

            msg.setText("Authentication fail.")
            msg.setInformativeText("Please re sign in.")
            msg.setWindowTitle("Warnning !!!")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.buttonClicked.connect(self.msgbtn)
            
            retval = msg.exec_()
            print ("value of pressed message box button:", retval)

class Thread(QThread):
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
                #p = QPixmap.fromImage(rgbImage)    
                #p = p.scaled(640, 480, Qt.KeepAspectRatio)
                convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QImage.Format_RGB888)
                p = convertToQtFormat.scaled(256, 256, Qt.KeepAspectRatio)
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
        self.stop()
        #self.quit()
        #self.terminate()
class HomeApp(QMainWindow):
    def __init__(self, parent=None):
        global uid
        global buttonDict
        
        QWidget.__init__(self, parent)
        self.ui = HomeScreen()
        self.ui.setupHomeScreen(self)
        self.ui.btn_0.clicked.connect(self.toHome)
        
        font = QFont()
        font.setPointSize(15) 
        all_users = db.child(uid).get()
        if all_users != None:
            with open('nodeInfo.json', 'w') as outfile:  
                json.dump(all_users.val(), outfile)
        #print("THIS IS DATA ::::: {}".format(str(all_users)))
        
        for user in all_users.each():
            print(user.key()) # Morty
            print(user.val())
            print(type(user.val())) # {name": "Mortimer 'Morty' Smith"}
            self.ui.pushButton = QtWidgets.QPushButton(self.ui.gridLayoutWidget)
            self.ui.pushButton.setFixedSize( 130, 100 )
            self.ui.pushButton.setObjectName(str(user.key()))
            self.ui.pushButton.setFont(font)
            self.ui.pushButton.setText(str(user.val().get("room")) + "\n type : " + str(user.val().get("type")))
            if user.val().get('status') == '0':
                self.ui.pushButton.setStyleSheet('background-color:#002330;color:#FFFFFF;') 
            else:
                self.ui.pushButton.setStyleSheet('background-color:#20BF55;color:#000000;') 
            #self.ui.pushButton.setStyleSheet("QPushButton { background-color:#002330; }"
            #                                    "QPushButton:pressed { background-color: #20BF55; }") 
            buttonDict[str(user.key())] = self.ui.pushButton
            self.ui.gridLayout.addWidget(self.ui.pushButton)
            self.ui.pushButton.clicked.connect(partial(self.buttonPress, user.key() , self.ui.pushButton))
        print(buttonDict)
    def toHome(self):
        self.close()
    def buttonPress(self,x,buttonObject):
        #buttonObject.setText("hello")
        global serRead
        global ser
        offForm = "!OFF,{}\r".format(x)
        onForm = "!ON,{}\r".format(x)
        now_state = db.child(uid).child(x).child('status').get()
        if now_state.val() == "0":
            try:
                serRead = False
                while ser.inWaiting()>0:
                    print("waiting for serial")
                ser.write(onForm.encode())
                serRead = True
            except:
                print("error to write command")
            buttonObject.setStyleSheet('background-color:#20BF55;color:#000000;') 
            db.child(uid).child(x).update({"status":"1"})
        else:
            try:
                serRead = False
                while ser.inWaiting()>0:
                    print("waiting for serial")
                ser.write(offForm.encode())
                serRead = True
            except:
                print("error to write command")
            buttonObject.setStyleSheet('background-color:#002330;color:#FFFFFF;')
            db.child(uid).child(x).update({"status":"0"})
            
        print(x)
    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Escape:
            print('esc')
            self.close()

class ThreadFingerCompare(QThread):
    state = pyqtSignal(int)
    def run(self):
        try:
            f = PyFingerprint(USB_FINGER_PORT, 57600, 0xFFFFFFFF, 0x00000000)

            if ( f.verifyPassword() == False ):
                raise ValueError('The given fingerprint sensor password is wrong!')
        except Exception as e:
            print('The fingerprint sensor could not be initialized!')
            print('Exception message: ' + str(e))
            self.state.emit(-1)
        try:
            print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))
        
            print('Waiting for finger...')
            while ( f.readImage() == False):
                time.sleep(0.3)
                pass
            f.convertImage(0x01)
            result = f.searchTemplate()
            positionNumber = result[0]
            accuracyScore = result[1]
            if ( positionNumber == -1 ):
                print('No match found!')
                self.state.emit(2)
                #return False
                #exit(0)
            else:
                print('Found template at position #' + str(positionNumber))
                print('The accuracy score is: ' + str(accuracyScore))
            f.loadTemplate(positionNumber, 0x01)
            characterics = str(f.downloadCharacteristics(0x01)).encode('utf-8')
            myHash = str(hashlib.sha256(characterics).hexdigest())
            print("the hash is :"+myHash)
            if positionNumber != -1: #if myHash == "293122122adcc20688174f49c8cb2a330523616b41fc505cacb5a1f841c7e146":
                print("finger print match !!")
                self.state.emit(1)
                # homeapp = HomeApp(self)
                # homeapp.show()
            else:
                print("finger print doesn't match")
                
                    
        except Exception as e:
            print('Operation failed!')
            print('Exception message: ' + str(e))
            self.state.emit(-1)
            #exit(1)
    def __del__(self):
        self.flag = False
        self.quit()
        self.wait()
    def stop(self):
        self.terminate()
        #self.stop()
class ThreadBLE(QThread):
    state = pyqtSignal(int)
    flag = True
    count = 0
    avg = 0
    try:
        sock = bluez.hci_open_dev(0)
        print("ble thread started")

    except:
        print("error accessing bluetooth device...")
        self.state.emit(-2)
    blescan3.hci_le_set_scan_parameters(sock)
    blescan3.hci_enable_le_scan(sock)
    startTime = time.time()
    currentTime = time.time()
    def run(self):
        self.startTime = time.time()
        while True:
            self.currentTime = time.time()
            pote_phone =  "7FA08BC7A55F45FC85C00BF26F899530"
            pote_beacon = pote_phone.lower()
            returnedList = blescan3.parse_events(self.sock, 10)
            if (self.currentTime-self.startTime)>=5:
                self.state.emit(-1)
                self.startTime = self.currentTime
                #print("5s interval")
            else:
                #returnedList = blescan3.parse_events(self.sock, 1)
                #print("----------")
                for beacon in returnedList:
                    #print("found pote beacon in thread")
                    if(pote_beacon in beacon):
                        arr = beacon.split(",")
                        txPower = float(arr[1])
                        rssi = float(arr[2])
                        distance = 10**((txPower-rssi)/(10.0*2.0))
                        self.avg += distance
                        beacon += ","
                        beacon += str(distance)
                        #print(beacon)
                        self.count += 1
                        if(self.count >= 5):
                            self.startTime = time.time()
                            self.state.emit(self.avg/5.0)
                            #print(pote_beacon)
                            #print("Average = " + str(self.avg/10.0))
                            self.count = 0
                            self.avg = 0
    def __del__(self):
        self.flag = False
        self.quit()
        self.wait()
    def stop(self):
        self.flag = False
        self.terminate()
        #self.stop()
class MyApp(QMainWindow):
    img1 = None
    @pyqtSlot(QImage)
    def setImage(self, image):
        #self.img1 = QPixmap.fromImage(image)
        self.ui.label_3.setPixmap(QPixmap.fromImage(image))
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.image = cv2.imread('images/facial.jpg')
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        self.convertToQtFormat = QImage(self.image.data, self.image.shape[1], self.image.shape[0], QImage.Format_RGB888)
        self.ui.label_3.setPixmap(QPixmap.fromImage(self.convertToQtFormat))
        self.ui.label_3.mousePressEvent = self.takePhoto
        self.thFingerCompare = ThreadFingerCompare(self)
        #self.thFingerCompare.setTerminationEnabled(True)
        self.thFingerCompare.state.connect(self.waitToScan)
        self.bleThread = ThreadBLE(self)
        self.bleThread.state.connect(self.bleCallback)
        self.bleThread.start()

        self.th = Thread(self)
        self.th.changePixmap.connect(self.setImage)
        self.th.state.connect(self.closeCam)
        self.th.take.connect(self.savePhoto)
        #self.th.setTerminationEnabled(True)
        self.th.start()
        
        with open('bleAuth.json') as json_file:
            try:
                data = json.load(json_file)
                print("ble auth file OK")
                print(data['bleID'])
            except:
                print("ble auth file invalid")
            
    def bleCallback(self,x):
        global bleAuth
        if x == -1:
            bleAuth = False
            print('BLE timeout')
            self.ui.label_beacon.setText("Beacon scanning..")
        elif x == -2:
            self.ui.label_beacon.setText("Beacon Error.")
        else:
            bleAuth = True
            print("BLE detected id is+{}".format(x))
            self.ui.label_beacon.setText("Beacon Detected")
    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Escape:
            print('esc')
            self.close()
    def waitToScan(self,x):
        if x == 1:
            #self.thFingerCompare.stop()
            homeapp = HomeApp(self)
            homeapp.showFullScreen()
        elif x == 2:
            #self.thFingerCompare.stop()
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("fingerprint doesn't match")
            msg.setInformativeText("please try again.")
            msg.setWindowTitle("Error.")
            msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_()
        elif x == -1:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("The fingerprint sensor could not be initialized!")
            msg.setInformativeText("please try again.")
            msg.setWindowTitle("Error.")
            msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_()

            
    def fingerScan(self,x):
        print("finger scan button clicked!")
        self.thFingerCompare.start()
        
    def closeCam(self):
        print("terminating.....")
        #if self.th.isRunning():
        self.th.stop()
        #self.th.terminate()
    def predict(self,img, knn_clf=None, model_path=None, distance_threshold=0.4):
            # if not os.path.isfile(X_img_path) or os.path.splitext(X_img_path)[1][1:] not in ALLOWED_EXTENSIONS:
            #     raise Exception("Invalid image path: {}".format(X_img_path))

            if knn_clf is None and model_path is None:
                raise Exception("Must supply knn classifier either thourgh knn_clf or model_path")

            # Load a trained KNN model (if one was passed in)
            if knn_clf is None:
                with open(model_path, 'rb') as f:
                    knn_clf = pickle.load(f)

            # Load image file and find face locations
            X_img =  img #face_recognition.load_image_file(X_img_path)
            X_face_locations = face_recognition.face_locations(X_img)

            # If no faces are found in the image, return an empty result.
            if len(X_face_locations) == 0:
                return []

            # Find encodings for faces in the test iamge
            faces_encodings = face_recognition.face_encodings(X_img, known_face_locations=X_face_locations)
            # face_distances = face_recognition.face_distance(faces_encodings, X_face_locations)
            # print(face_distances)
            # Use the KNN model to find the best matches for the test face
            closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=1)
            are_matches = [closest_distances[0][i][0] <= distance_threshold for i in range(len(X_face_locations))]
            print(closest_distances)
            # Predict classes and remove classifications that aren't within the threshold
            return [(pred, loc) if rec else ("unknown", loc) for pred, loc, rec in zip(knn_clf.predict(faces_encodings), X_face_locations, are_matches)]
    def savePhoto(self,img1):
            print(type(img1))
            global faceAuth
            global passAuth
            global bleAuth
            global fingerAuth
            #img1.save('tmp.png','PNG')
            cv2.imwrite("tmppic.jpg", img1)
            flag = False
            try:
                fh = open('trained_knn_model.clf', 'r')
                fh.close()
                flag=True
            except FileNotFoundError:
                QMessageBox.about(self, "Info", "Unable to locate faces.")
                # Keep preset values
            if flag:
                predictions = self.predict(img1, model_path='trained_knn_model.clf')
                if(len(predictions) >= 1):
                    for name, (top, right, bottom, left) in predictions:
                            print("- Found {} at ({}, {})".format(name, left, top))
                            if name != "unknown":
                                    faceAuth = True
                                    self.ui.label_3.setPixmap(QPixmap.fromImage(self.convertToQtFormat))
                                    self.ui.btn_photo.setText(name)
                                    self.ui.btn_photo.setStyleSheet('QPushButton {background-color: #A3C1DA; color: green;}')
                                    if faceAuth+passAuth+bleAuth+fingerAuth >= 2:
                                            faceAuth,passAuth,bleAuth,fingerAuth = False,False,False,False
                                            homeapp = HomeApp(self)
                                            homeapp.showFullScreen()
                                    else:
                                            QMessageBox.about(self, "Info", "Please authenicate with 1 more method")
                            else:
                                    print("Unknown !!!!")
                                    QMessageBox.about(self, "Info", "Face doesn't match")
                                    self.ui.btn_photo.setText("Take photo")
                                    self.ui.btn_photo.setStyleSheet('QPushButton {background-color: #A3C1DA; color: red;}')
                                    
                else:
                        print("not match")
                        QMessageBox.about(self, "Info", "Face doesn't match")
                        self.ui.btn_photo.setText("Take photo")
                        self.ui.btn_photo.setStyleSheet('QPushButton {background-color: #A3C1DA; color: black;}')
                print("photo saved!")
    def takePhoto(self,event):
        self.th.take_photo()
        # flag = False
        # try:
        #     fh = open('trained_knn_model.clf', 'r')
        #     fh.close()
        #     flag=True
        # except FileNotFoundError:
        #     msgBox = QMessageBox()
        #     msgBox.setText("Error")
        #     msgBox.setInformativeText("Unable to locate faces. Do you want to add a new face")
        #     msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        #     msgBox.setDefaultButton(QMessageBox.Yes)
        #     ret = msgBox.exec_()
        #     if ret == QMessageBox.Yes:
        #         print("Yes!!!!")
        #     elif ret == QMessageBox.Cancel:
        #         print("Nooooooooo!!!!")
        #     #QMessageBox.about(self, "Info", "Unable to locate faces.")
        #     # Keep preset values
        # if flag:
        #     #print("Taking photos...")
        #     # self.th = Thread(self)
        #     # self.th.changePixmap.connect(self.setImage)
        #     # self.th.state.connect(self.closeCam)
            
        #     # self.th.take.connect(self.savePhoto)
            
        #     # self.th.setTerminationEnabled(True)
        #     # self.th.start()
        #     self.ui.btn_photo.setEnabled(False)
        #     self.ui.btn_photo.setStyleSheet('QPushButton {background-color: #A3C1DA; color: black;}')
        #     QTimer.singleShot(4200, lambda: self.th.stop())
        #     QTimer.singleShot(5500, lambda: self.ui.label_3.setPixmap(QPixmap.fromImage(self.convertToQtFormat)))
        #     QTimer.singleShot(4000, lambda: self.ui.btn_photo.setDisabled(False))
        #     QTimer.singleShot(1000, lambda: self.ui.btn_photo.setText("Hold..(3)"))
        #     QTimer.singleShot(2000, lambda: self.ui.btn_photo.setText("Hold..(2)"))
        #     QTimer.singleShot(3000, lambda: self.ui.btn_photo.setText("Hold..(1)"))
        #     QTimer.singleShot(3500, lambda: self.th.take_photo())
        #QTimer.singleShot(7100, lambda: self.ui.btn_photo.setText("Take a photo"))
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
        global faceAuth
        global passAuth
        global bleAuth
        global fingerAuth
        global passcodes
        with open('pass.json') as json_file:
            json_pass = json.load(json_file)
        if(len(passcodes) >= 4):
            hash_object = hashlib.sha256(passcodes.encode())
            hex_dig = hash_object.hexdigest()
            if(hex_dig == json_pass["pass"]):
                self.ui.password_field.setStyleSheet('color: green')
                print('Correct')
                #self.hide()
                passAuth = True
                if faceAuth+passAuth+bleAuth+fingerAuth >= 2:
                        faceAuth,passAuth,bleAuth,fingerAuth = False,False,False,False
                        passcodes = ""
                        self.ui.password_field.setStyleSheet('color: white')
                        self.ui.password_field.setText("")
                        homeapp = HomeApp(self)
                        homeapp.showFullScreen()
                        
                else:
                    passcodes = ""
                    #self.ui.password_field.setText("")
                    QMessageBox.about(self, "Info", "Please authenicate with 1 more method")
            else:
                self.ui.password_field.setStyleSheet('color: white')
                print('Wrong')
                passcodes = ''
                #self.ui.password_field.setText("")
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Password incorrect!!")
                #msg.setInformativeText("You are ready to go.")
                msg.setWindowTitle("Success.")
                msg.setStandardButtons(QMessageBox.Ok)
                retval = msg.exec_()
                self.printPasscode() 
    def train(train_dir, model_save_path=None, n_neighbors=None, knn_algo='ball_tree', verbose=False):
            X = []
            y = []

            # Loop through each person in the training set
            for class_dir in os.listdir(train_dir):
                if not os.path.isdir(os.path.join(train_dir, class_dir)):
                    continue

                # Loop through each training image for the current person
                for img_path in image_files_in_folder(os.path.join(train_dir, class_dir)):
                    image = face_recognition.load_image_file(img_path)
                    face_bounding_boxes = face_recognition.face_locations(image)

                    if len(face_bounding_boxes) != 1:
                        # If there are no people (or too many people) in a training image, skip the image.
                        if verbose:
                            print("Image {} not suitable for training: {}".format(img_path, "Didn't find a face" if len(face_bounding_boxes) < 1 else "Found more than one face"))
                    else:
                        # Add face encoding for current image to the training set
                        X.append(face_recognition.face_encodings(image, known_face_locations=face_bounding_boxes)[0])
                        y.append(class_dir)

            # Determine how many neighbors to use for weighting in the KNN classifier
            if n_neighbors is None:
                n_neighbors = int(round(math.sqrt(len(X))))
                if verbose:
                    print("Chose n_neighbors automatically:", n_neighbors)

            # Create and train the KNN classifier
            knn_clf = neighbors.KNeighborsClassifier(n_neighbors=n_neighbors, algorithm=knn_algo, weights='distance')
            knn_clf.fit(X, y)

            # Save the trained KNN classifier
            if model_save_path is not None:
                with open(model_save_path, 'wb') as f:
                    pickle.dump(knn_clf, f)

            return knn_clf

class PasswordSettingApp(QMainWindow):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        font = QFont()
        font.setPointSize(16) 
        self.passCode = ""
        self.passDict = {}
        self.firstPass = ""
        self.secondPass = ""
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        ### hide not use ###
        self.ui.btn_finger.hide()
        self.ui.btn_photo.hide()
        self.ui.label_beacon.hide()
        self.ui.label_2.hide()
        self.ui.label_3.setFont(font)
        self.ui.label_3.setStyleSheet("color:#FFFFFF;")
        self.ui.label_3.setText("Type your 4 digit password.")


    def enterCode(self, n) :
        #print("password entered : {}".format(n))
        self.passCode += n
        lenn = len(self.passCode)
        if lenn >=4:
            
            if len(self.firstPass) <=0:
                self.firstPass = self.passCode 
                self.passCode = ""
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)

                msg.setText("Re type your 4 digit password.")
                #msg.setInformativeText("")
                msg.setWindowTitle("Success.")
                msg.setStandardButtons(QMessageBox.Ok)
                retval = msg.exec_()
                self.ui.label_3.setText("Type your 4 digit password again.")
                self.ui.password_field.setText('')
                self.ui.password_field.repaint()
            else:
                if self.passCode == self.firstPass:
                    self.ui.password_field.setText('')
                    self.ui.password_field.repaint()
                    hash_object = hashlib.sha256(self.passCode.encode())
                    hex_dig = hash_object.hexdigest()
                    self.passDict["pass"] = hex_dig
                    # pass_json = json.dumps(self.passDict)
                    with open('pass.json', 'w') as outfile:  
                        json.dump(self.passDict, outfile)
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Password saved.")
                    msg.setInformativeText("You are ready to go.")
                    msg.setWindowTitle("Success.")
                    msg.setStandardButtons(QMessageBox.Ok)
                    retval = msg.exec_()
                    myappDash = MyApp()
                    myappDash.showFullScreen()
                    self.close()


        else:
            self.ui.password_field.setText(self.passCode)
            self.ui.password_field.repaint()
    def enterDelete(self) :
        print("password entered : DEL")
    def fingerScan(self):
        print("dummy!")
    def takePhoto(self):
        print("dummy2")
    

def stream_handler(message):
    global buttonDict
    global serRead
    global delayTime
    if type(message["data"]) is dict:
        # print("first run value")
        # print(message["data"])
        #print(message["path"])
        nodeID = message["path"].replace("/","")
        #print(nodeID)
        offForm = "!OFF,{}\r".format(nodeID)
        onForm = "!ON,{}\r".format(nodeID)
        #print("tag 5555")
        if len(message["data"]) <= 1:
            print("tag 1111")
            if buttonDict:
                buttonStrem = buttonDict.get(nodeID)
            print(type(buttonStrem))
            if message["data"]["status"] == "0":
                if buttonDict:
                    buttonStrem.setStyleSheet('background-color:#002330;color:#FFFFFF;')
                time.sleep(delayTime)
                try:
                    serRead = False
                    while ser.inWaiting()>0:
                        print("waiting for serial")
                    ser.write(offForm.encode())
                    serRead = True
                except:
                    print("error to write command")
                print('serial write off1')
            else:
                if buttonDict:
                    buttonStrem.setStyleSheet('background-color:#20BF55;color:#000000;') 
                time.sleep(delayTime)
                try:
                    serRead = False
                    while ser.inWaiting()>0:
                        print("waiting for serial")
                    ser.write(onForm.encode())
                    serRead = True
                except:
                    print("error to write command")
                #time.sleep(2)
                print('serial write on1')
        else:
            for x,y in message["data"].items():
                print(x)
                print(y["status"])
                if y["status"] == "0":
                    time.sleep(delayTime)
                    offForm2 = "!OFF,{}".format(x)
                    try:
                        serRead = False
                        while ser.inWaiting()>0:
                            print("waiting for serial")
                        ser.write(offForm2.encode())
                        serRead = True
                    except:
                        print("error to write command")
                    #time.sleep(2)
                    #ser.flushInput()
                    print('serial write off1')
                else:
                    time.sleep(delayTime)
                    onForm2 = "!ON,{}".format(x)
                    try:
                        serRead = False
                        while ser.inWaiting()>0:
                            print("waiting for serial")
                        ser.write(onForm2.encode())
                        serRead = True
                    except:
                        print("error to write command")

                    #time.sleep(2)
                    #ser.flushInput()
                    print('serial write on1')
            
    else:
        if message["path"].split("/")[2] == "status":
            print("updated node id is {} value is {}".format(message["path"].split("/")[1],message["data"]))
            if message["data"] == "0":
                offForm3 = "!OFF,{}".format(message["path"].split("/")[1])
                time.sleep(delayTime)
                #time.sleep()
                try:
                    serRead = False
                    while ser.inWaiting()>0:
                        print("waiting for serial")
                    ser.write(offForm3.encode())
                    serRead = True
                except:
                    print("error to write command")
                print('serial write off2')
            else:
                onForm3 = "!ON,{}".format(message["path"].split("/")[1])
                time.sleep(delayTime)
                try:
                    serRead = False
                    while ser.inWaiting()>0:
                        print("waiting for serial")
                    ser.write(onForm3.encode())
                    serRead = True
                except:
                    print("error to write command ")
                print('serial write on2')

# if uid != "":
#     my_stream = db.child(uid).stream(stream_handler)

connected = False
def handle_data(data):
    print(data)
def read_from_port(ser):
    global serRead 
    while True:
        if serRead:
            reading = ser.readline().decode()
            print("from ESP :{}".format(reading))
        else:
            print("serial now pause...")

thread = threading.Thread(target=read_from_port, args=(ser,))
thread.start()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    with open('auth.json') as json_file:
        # global uid
        # global auth
        try:
            data = json.load(json_file)
            print(data['user'])
            print(data['password'])
            try:
                user = auth.sign_in_with_email_and_password(data['user'], data['password'])
                    # before the 1 hour expiry:
                user = auth.refresh(user['refreshToken'])
                    # now we have a fresh token
                uid = user['userId']
                print(user['userId'])
                if uid != "":
                    my_stream = db.child(uid).stream(stream_handler)
                myappDash = MyApp()
                myappDash.showFullScreen()
                
            except:
                print('some error')
        except:
            myapp = MyAppSignIn()
            myapp.showFullscreen()
    
    # myapp = MyApp()
    # myapp.show()
    sys.exit(app.exec_())
