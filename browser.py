
import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLineEdit
from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtNetwork import  QNetworkProxy



class BrowserViewer(QWidget):
    def __init__(self):
        super().__init__()

        

        # Where the webpage is rendered.
        self.webview = QWebEngineView()
        self.webview.load(QUrl(""))# replace with your shotgrid URL
        self.webview.urlChanged.connect(self.url_changed)

         # Navigation buttons.
        self.back_button = QPushButton("<")
        self.back_button.clicked.connect(self.webview.back)
        self.forward_button = QPushButton(">")
        self.forward_button.clicked.connect(self.webview.forward)
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.webview.reload)

        # URL address bar.
        self.url_text = QLineEdit()

        # Button to load the current page.
        self.go_button = QPushButton("Go")
        self.go_button.clicked.connect(self.url_set)

        self.toplayout = QHBoxLayout()
        self.toplayout.addWidget(self.back_button)
        self.toplayout.addWidget(self.forward_button)
        self.toplayout.addWidget(self.refresh_button)
        self.toplayout.addWidget(self.url_text)
        self.toplayout.addWidget(self.go_button)

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.toplayout)
        self.layout.addWidget(self.webview)

        self.setLayout(self.layout)

    def url_changed(self, url):
        """Refresh the address bar"""
        self.url_text.setText(url.toString())

    def url_set(self):
        """Load the new URL"""
        self.webview.setUrl(QUrl(self.url_text.text()))



