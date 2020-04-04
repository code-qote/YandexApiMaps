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
        self.z = 17
        self.installEventFilter(self)
    
    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_PageDown:
            if self.z > 0:
                self.z -= 1
                self.search_with_coords(self.CurrentLongitude, self.CurrentLattitude) 
        elif event.type() == QEvent.KeyPress and event.key() == Qt.Key_PageUp:
            if self.z < 17:
                self.z += 1
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
            'z': str(self.z),
            'l': 'map',
            'pt': f'{longitude},{lattitude},pm2bll'
        }

        try:
            response = requests.get(map_server, params=search_params)
        except:
            return

        map_file = 'map.png'
        with open(map_file, 'wb') as file:
            file.write(response.content)
        
        self.MAP.setPixmap(QPixmap('map.png'))
                

