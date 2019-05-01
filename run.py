#!/usr/bin/python3
import sys
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

import math
from sklearn import neighbors
import os
import os.path
import pickle
from PIL import Image, ImageDraw
import face_recognition
from face_recognition.face_recognition_cli import image_files_in_folder
import pyrebase
import json
import serial
import threading
import time

from pyzbar import pyzbar
from signinscreen import Ui_SignIn
USB_FINGER_PORT = '/dev/ttyUSB0'
authEmail = ""
authPass = ""
port = '/dev/tty.usbserial-1410'
baud = 115200
ser = serial.Serial(port, baud)
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

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
passAuth = False
faceAuth = False
fingerAuth = False
bleAuth = False
### this is gun comment ###
passcodes = ''
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
class MyAppSignIn(QMainWindow):
    img1 = None
    @pyqtSlot(QImage)
    def setImage(self, image):
        self.ui.label_2.setPixmap(QPixmap.fromImage(image))
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = Ui_SignIn()
        self.ui.setupUi(self)
        self.blank_image = np.zeros((350,350,3), np.uint8)
        cv2.putText(self.blank_image,"Welcome", (40,50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255,255,255))
        self.convertToQtFormat = QImage(self.blank_image.data, self.blank_image.shape[1], self.blank_image.shape[0], QImage.Format_RGB888)
        self.ui.label_2.setPixmap(QPixmap.fromImage(self.convertToQtFormat))
        
        self.th = ThreadQR(self)
        self.th.changePixmap.connect(self.setImage)
        self.th.state.connect(self.authPass)
        self.th.start()
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
            myappDash = MyApp()
            myappDash.show()
            self.close()
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
            #self.quit()
            #self.terminate()
class HomeApp(QMainWindow):
    def __init__(self, parent=None):
        global uid
        QWidget.__init__(self, parent)
        self.ui = HomeScreen()
        self.ui.setupHomeScreen(self)
        font = QFont()
        font.setPointSize(18) 
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
            
            self.ui.gridLayout.addWidget(self.ui.pushButton)
            self.ui.pushButton.clicked.connect(partial(self.buttonPress, user.key() , self.ui.pushButton))
    def buttonPress(self,x,buttonObject):
        #buttonObject.setText("hello")
        global ser
        offForm = "!OFF,{}".format(x)
        onForm = "!ON,{}".format(x)
        now_state = db.child(uid).child(x).child('status').get()
        if now_state.val() == "0":
            buttonObject.setStyleSheet('background-color:#20BF55;color:#000000;') 
            db.child(uid).child(x).update({"status":"1"})
            ser.write(onForm.encode())
        else:
            buttonObject.setStyleSheet('background-color:#002330;color:#FFFFFF;')
            db.child(uid).child(x).update({"status":"0"})
            ser.write(offForm.encode())
        print(x)
    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Escape:
            print('esc')
            self.close()
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
    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Escape:
            print('esc')
            self.close()
    def waitToScan(self):
        print("wait to scan")
        try:
            f = PyFingerprint(USB_FINGER_PORT, 57600, 0xFFFFFFFF, 0x00000000)

            if ( f.verifyPassword() == False ):
                raise ValueError('The given fingerprint sensor password is wrong!')
        except Exception as e:
            print('The fingerprint sensor could not be initialized!')
            print('Exception message: ' + str(e))
            exit(1)
        print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))
        try:
            print('Waiting for finger...')
            while ( f.readImage() == False ):
                pass
            f.convertImage(0x01)
            result = f.searchTemplate()
            positionNumber = result[0]
            accuracyScore = result[1]
            if ( positionNumber == -1 ):
                print('No match found!')
                return False
                #exit(0)
            else:
                print('Found template at position #' + str(positionNumber))
                print('The accuracy score is: ' + str(accuracyScore))
            f.loadTemplate(positionNumber, 0x01)
            characterics = str(f.downloadCharacteristics(0x01)).encode('utf-8')
            myHash = str(hashlib.sha256(characterics).hexdigest())
            print("the hash is :"+myHash)
            if myHash == "cfce640e78de26420c6247705e9c975004415a583a0e4ad6202eb46f283db8e7":
                    print("finger print match !!")
                    homeapp = HomeApp(self)
                    homeapp.show()
            else:
                    print("finger print doesn't match")
        except Exception as e:
            print('Operation failed!')
            print('Exception message: ' + str(e))
            exit(1)
            
    def fingerScan(self,x):
        print("finger scan button clicked!")
        self.waitToScan()
    def closeCam(self):
        print("terminating.....")
        if self.th.isRunning():
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
                                        homeapp.show()
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
        print("Taking photos...")
        self.th = Thread(self)
        self.th.changePixmap.connect(self.setImage)
        self.th.state.connect(self.closeCam)
        
        self.th.take.connect(self.savePhoto)
        
        self.th.setTerminationEnabled(True)
        self.th.start()
        self.ui.btn_photo.setEnabled(False)
        self.ui.btn_photo.setStyleSheet('QPushButton {background-color: #A3C1DA; color: black;}')
        QTimer.singleShot(4200, lambda: self.th.stop())
        QTimer.singleShot(5500, lambda: self.ui.label_3.setPixmap(QPixmap.fromImage(self.convertToQtFormat)))
        QTimer.singleShot(4000, lambda: self.ui.btn_photo.setDisabled(False))
        QTimer.singleShot(1000, lambda: self.ui.btn_photo.setText("Hold..(3)"))
        QTimer.singleShot(2000, lambda: self.ui.btn_photo.setText("Hold..(2)"))
        QTimer.singleShot(3000, lambda: self.ui.btn_photo.setText("Hold..(1)"))
        QTimer.singleShot(3500, lambda: self.th.take_photo())
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
        if(len(passcodes) >= 4):
            if(passcodes == '1234'):
                self.ui.password_field.setStyleSheet('color: green')
                print('Correct')
                #self.hide()
                passAuth = True
                if True:#faceAuth+passAuth+bleAuth+fingerAuth >= 2:
                        faceAuth,passAuth,bleAuth,fingerAuth = False,False,False,False
                        homeapp = HomeApp(self)
                        homeapp.show()
                else:
                        QMessageBox.about(self, "Info", "Please authenicate with 1 more method")
            else:
                self.ui.password_field.setStyleSheet('color: black')
                print('Wrong')
                passcodes = ''
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
 
def stream_handler(message):
    if type(message["data"]) is dict:
        # print("first run value")
        # print(message["data"])
        #print(message["path"])
        nodeID = message["path"].replace("/","")
        print(nodeID)
        offForm = "!OFF,{}".format(nodeID)
        onForm = "!ON,{}".format(nodeID)
        if len(message["data"]) <= 1:
            if message["data"]["status"] == "0":
                ser.write(offForm.encode())
                print('serial write off')
            else:
                ser.write(onForm.encode())
                print('serial write on')
        else:
            for x,y in message["data"].items():
                print(x)
                print(y["status"])
                if y["status"] == "0":
                    offForm2 = "!OFF,{}".format(x)
                    ser.write(offForm2.encode())
                    time.sleep(1)
                    #ser.flushInput()
                    print('serial write off')
                else:
                    onForm2 = "!ON,{}".format(x)
                    ser.write(onForm2.encode())
                    time.sleep(1)
                    #ser.flushInput()
                    print('serial write on')
            
    else:
        if message["path"].split("/")[2] == "status":
            print("updated node id is {} value is {}".format(message["path"].split("/")[1],message["data"]))
            if message["data"] == "0":
                offForm3 = "!OFF,{}".format(message["path"].split("/")[1])
                ser.write(offForm3.encode())
                print('serial write off')
            else:
                onForm3 = "!ON,{}".format(message["path"].split("/")[1])
                ser.write(onForm3.encode())
                print('serial write on')

if uid != "":
    my_stream = db.child(uid).stream(stream_handler)

connected = False
def handle_data(data):
    print(data)
def read_from_port(ser):
        while True:
            reading = ser.readline().decode()
            print("from ESP :{}".format(reading))

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
                myappDash = MyApp()
                myappDash.show()
                
            except:
                print('some error')
        except:
            myapp = MyAppSignIn()
            myapp.show()
    
    # myapp = MyApp()
    # myapp.show()
    sys.exit(app.exec_())
