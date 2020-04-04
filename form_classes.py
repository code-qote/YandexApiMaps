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
        self.BSearch.clicked.connect(self.search_with_coords)
        self.spn = '2'

    def search_with_coords(self):
        try:
            longitude = float(self.LELongitude.text())
        except TypeError:
            self.LELongitude.setText('Error')
            return
        
        try:
            lattitude = float(self.LELattitude.text())
        except TypeError:
            self.LELattitude.setText('Error')
            return

        search_params = {
            'll': f'{longitude},{lattitude}',
            'spn': f'{self.spn},{self.spn}',
            'l': 'map',
            'pt': f'{longitude},{lattitude},pm2bll'
        }

        try:
            response = requests.get(map_server, params=search_params)
        except:
            print('f')
            return

        map_file = 'map.png'
        with open(map_file, 'wb') as file:
            file.write(response.content)
        
        self.MAP.setPixmap(QPixmap('map.png'))
                

