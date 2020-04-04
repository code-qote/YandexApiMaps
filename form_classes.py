from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from fmain import Ui_fmain
from consts import *
import requests
from io import BytesIO


class MainForm(QMainWindow, Ui_fmain):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.config()

    def config(self):
        self.BSearch.clicked.connect(self.start_search)
        self.spn = 0.01
        self.installEventFilter(self)
        #test
        self.CurrentLattitude = 53.2
        self.CurrentLongitude = 50.15
        #test
        self.search_with_coords(self.CurrentLongitude, self.CurrentLattitude)
    
    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_PageDown:
            if self.spn > 0.0001:
                self.spn /= 10
                self.search_with_coords(self.CurrentLongitude, self.CurrentLattitude) 
        elif event.type() == QEvent.KeyPress and event.key() == Qt.Key_PageUp:
            if self.spn < 50:
                if self.spn >= 10:
                    self.spn *= 2
                else:
                    self.spn *= 10
                self.search_with_coords(self.CurrentLongitude, self.CurrentLattitude)
        elif event.type() == QEvent.KeyPress and event.key() == Qt.Key_Up:
            if self.CurrentLattitude + self.spn < 90:
                self.CurrentLattitude += self.spn
            self.search_with_coords(self.CurrentLongitude, self.CurrentLattitude)
        elif event.type() == QEvent.KeyPress and event.key() == Qt.Key_Down:
            if self.CurrentLattitude - self.spn > -90:
                self.CurrentLattitude -= self.spn
            self.search_with_coords(self.CurrentLongitude, self.CurrentLattitude)
        elif event.type() == QEvent.KeyPress and event.key() == Qt.Key_Right:
            if self.CurrentLongitude + self.spn < 180:
                self.CurrentLongitude += self.spn
            self.search_with_coords(self.CurrentLongitude, self.CurrentLattitude)
        elif event.type() == QEvent.KeyPress and event.key() == Qt.Key_Left:
            if self.CurrentLongitude - self.spn > -180:
                self.CurrentLongitude -= self.spn
            self.search_with_coords(self.CurrentLongitude, self.CurrentLattitude)
        return QWidget.eventFilter(self, obj, event)
    
    def start_search(self):
        try:
            self.CurrentLongitude = float(self.LELongitude.text())
        except TypeError:
            self.LELongitude.setText('Error')
            return

        try:
            self.CurrentLattitude = float(self.LELattitude.text())
        except TypeError:
            self.LELattitude.setText('Error')
            return
        
        self.search_with_coords(self.CurrentLongitude, self.CurrentLattitude)

    def search_with_coords(self, longitude, lattitude):
        search_params = {
            'll': f'{longitude},{lattitude}',
            'spn': f'{self.spn},{self.spn}',
            'l': 'map'
        }

        try:
            response = requests.get(map_server, params=search_params)
        except:
            return

        map_file = 'map.png'
        with open(map_file, 'wb') as file:
            file.write(response.content)
        print(self.CurrentLongitude, self.CurrentLattitude)
        
        self.MAP.setPixmap(QPixmap('map.png'))
                

