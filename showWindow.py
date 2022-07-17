import sys
import cv2 as cv
import numpy as np
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from dataCleaner import resizeMovie

class MainWindow(QWidget):
    """
        Sets up the User interface and starts the worker thread for viewing the video.
    """
    def __init__(self, filePath, useTrained):
        super(MainWindow, self).__init__()
        self.vbl = QGridLayout()
        self.feedLabel = QLabel()
        self.setupUI()
        self.setLayout(self.vbl)
        self.path = resizeMovie(filePath) if filePath != True else "Subject\\video.mp4"
        self.worker = HogWorker(self.path) if not useTrained else CasWorker(self.path)
        self.worker.imgSignal.connect(self.updateImgSlot)
        self.worker.start()

    def setupUI(self):
        self.vbl.addWidget(self.feedLabel, 0,0,1,3, Qt.AlignmentFlag.AlignCenter)
        self.pauseBtn = QPushButton("Pause")
        self.playBtn = QPushButton("Play")
        self.exitBtn = QPushButton("Exit")
        self.pauseBtn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.playBtn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.exitBtn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.pauseBtn.clicked.connect(self.on_pause_click)
        self.playBtn.clicked.connect(self.playVideo)
        self.exitBtn.clicked.connect(self.end)
        self.pauseBtn.setMaximumWidth(70)
        self.playBtn.setMaximumWidth(70)
        self.exitBtn.setMaximumWidth(70)
        
        self.vbl.addWidget(self.pauseBtn, 1,0, Qt.AlignmentFlag.AlignCenter)
        self.vbl.addWidget(self.playBtn,  1,1, Qt.AlignmentFlag.AlignCenter)
        self.vbl.addWidget(self.exitBtn,  1,2, Qt.AlignmentFlag.AlignCenter)

    def updateImgSlot(self, image):
        self.feedLabel.setPixmap(QPixmap.fromImage(image))
    
    # pause the video
    def on_pause_click(self):
        self.worker.pause()

    # end the program
    def end(self):
        self.worker.stop()
        self.close()

    # resume the video
    def playVideo(self):
        self.worker.play()

    # we stop the thread before the application exits 
    def closeEvent(self, a0: QCloseEvent) -> None:
        self.worker.stop()
        return super().closeEvent(a0)

class HogWorker(QThread):
    def __init__(self, fileName):
        self.fileName = fileName
        super().__init__()

    imgSignal = pyqtSignal(QImage)
    speed = 30
    frameIndex = 0
    
    def run(self):
        self.running = True
        self.showVideo(self.fileName)

    def showVideo(self, fileName, frameStart = 0):
        hog = cv.HOGDescriptor()
        hog.setSVMDetector(cv.HOGDescriptor_getDefaultPeopleDetector())

        cv.startWindowThread()
        cap = cv.VideoCapture(fileName)
        cap.set(cv.CAP_PROP_POS_FRAMES, frameStart)
        

        while cap.isOpened() and self.running:
            ret, frame = cap.read()
            if not ret: break

            cv.waitKey(self.speed)
            gray = cv.cvtColor(frame, cv.COLOR_RGB2GRAY)

            people, weights = hog.detectMultiScale(gray, winStride = (8, 8))
          
            people = np.array([[x, y, x + width, y + height] for (x, y, width, height) in people])

            for (x1, y1, x2, y2) in people:
                cv.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
            qtFormatted = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format.Format_BGR888)
            self.imgSignal.emit(qtFormatted)
            self.frameIndex += 1


        cap.release()

        cv.destroyAllWindows()

    # stop the thread
    def stop(self):
        self.running = False
        self.quit()

    def pause(self):
        self.running = False

    def play(self):
        self.running =True
        self.showVideo(self.fileName, frameStart=self.frameIndex)


class CasWorker(QThread):
    def __init__(self, fileName):
        self.fileName = fileName
        super().__init__()



    