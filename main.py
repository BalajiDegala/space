
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QProgressBar, QFrame

from PyQt5.QtCore import Qt,pyqtSignal,QTimer, QRect, QThread
from PyQt5.QtGui import QFont, QIcon

import sys
import os
import time
from utils import *
from app import TaskViewer
## ==> GLOBALS
counter = 0
USER = os.getenv("USER")


class SplashScreen(QMainWindow):
    def __init__(self):
        super(SplashScreen, self).__init__()
        self.resize(750, 400)
        self.centralwidget = QWidget()
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(100, 50, 25, 10)
        self.dropShadowFrame = QFrame(self.centralwidget)
        self.dropShadowFrame.setStyleSheet("QFrame { border-radius: 10px; background-color: rgb(56, 58, 89); color: rgb(220, 220, 220);}")
        self.dropShadowFrame.setFrameShape(QFrame.StyledPanel)
        self.dropShadowFrame.setFrameShadow(QFrame.Raised)

        self.progressBar = QProgressBar(self.dropShadowFrame)
        self.progressBar.setTextVisible(0)
        self.progressBar.setGeometry(QRect(6, 180, 610, 40))
        self.progressBar.setStyleSheet("QProgressBar { background-color: rgb(98, 114, 164); color: rgb(200, 200, 200);text-align: center; } QProgressBar::chunk{ background-color: rgb(56, 58, 89);}")

        self.label_title = QLabel(self.dropShadowFrame)
        self.label_title.setGeometry(QRect(0, 50, 661, 61))
        font = QFont()
        font.setFamily("univers")
        font.setPointSize(40)
        self.label_title.setFont(font)
        self.label_title.setStyleSheet(u"color: rgb(254, 121, 199);")
        self.label_title.setAlignment(Qt.AlignCenter)
        self.label_title.setText(" S  P  A  C  E ")

        self.label_description = QLabel(self.dropShadowFrame)
        self.label_description.setGeometry(QRect(0, 120, 661, 31))
        font1 = QFont()
        font1.setFamily("Segoe UI")
        font1.setPointSize(15)
        self.label_description.setFont(font1)
        self.label_description.setStyleSheet(u"color: rgb(98, 114, 164);")
        self.label_description.setAlignment(Qt.AlignCenter)

        self.label_loading = QLabel(self.dropShadowFrame)
        self.label_loading.setGeometry(QRect(0, 280, 661, 21))
        font2 = QFont()
        font2.setFamily("Segoe UI")
        font2.setPointSize(10)
        self.label_loading.setFont(font2)
        self.label_loading.setStyleSheet(u"color: rgb(98, 114, 164);")
        self.label_loading.setAlignment(Qt.AlignCenter)
        self.label_loading.setText(" W  O  R  K       S  P  A  C  E")

        self.verticalLayout.addWidget(self.dropShadowFrame)
        self.setCentralWidget(self.centralwidget)

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.timer = QTimer()
        self.timer.timeout.connect(self.progress)
        self.timer.start(25)

        space_user_l = []
        for i in USER.upper():
            space_user_l.append(i)
            space_user_l.append("  ")

        space_user = "".join(space_user_l)

        self.label_description.setText( space_user )


        self.show()

    def progress(self):

        global counter
        self.progressBar.setValue(counter)
        if counter > 100:
            self.timer.stop()
            then = time.time()
            self.main = TaskViewer()
            self.main.show()
            now = time.time()
            print(now - then)
            self.close()
        counter += 1




if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    app.setStyleSheet(open('resources/css/login.qss').read())
    # app.setWindowIcon(QIcon('')) #Replace with your logo 
    window = SplashScreen()
    window.show()
    sys.exit(app.exec_())

