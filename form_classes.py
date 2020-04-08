from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from fmain import Ui_fmain
from consts import *
import requests
import os
import geocoder
from functools import partial
from io import BytesIO


class MainForm(QMainWindow, Ui_fmain):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.config()
    
    def updateMapType(self, Mtype, map_file):
        self.mapType = Mtype
        self.map_file = map_file
        self.search_with_coords(self.CurrentLongitude, self.CurrentLattitude, self.CurrentPoints)

    def deletePoint(self):
        self.isPoint = False
        self.CurrentPoint = None
        self.LELSearch.clear()
        self.LEAddress.clear()
        self.search_with_coords(self.CurrentLongitude, self.CurrentLattitude, self.isPoint)
    
    def updateSearch(self): 
        self.isSearchNearMe = not(self.isSearchNearMe)

    def config(self):
        self.BSearch.clicked.connect(self.start_search)
        self.BCancel.clicked.connect(self.deletePoint)
        self.BSearch.setAutoDefault(True)
        self.isSearchNearMe = False
        self.RBSearchNearMe.toggled.connect(self.updateSearch)
        self.LELSearch.returnPressed.connect(self.BSearch.click)
        self.spn = 0.01
        self.CurrentPoints = []
        self.installEventFilter(self)
        self.CurrentLattitude, self.CurrentLongitude = geocoder.ip('me').latlng
        self.mapType = 'map'
        self.map_file = 'map.png'
        self.BMap.clicked.connect(partial(self.updateMapType, Mtype='map', map_file='map.png'))
        self.BSat.clicked.connect(partial(self.updateMapType, Mtype='sat', map_file='map.jpg'))
        self.BSkl.clicked.connect(partial(self.updateMapType, Mtype='sat,skl', map_file='map.jpg'))
        self.search_with_coords(self.CurrentLongitude, self.CurrentLattitude)
    
    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_PageDown:
            if self.spn > 0.0001:
                self.spn /= 10
                self.search_with_coords(self.CurrentLongitude, self.CurrentLattitude, self.CurrentPoints) 
        elif event.type() == QEvent.KeyPress and event.key() == Qt.Key_PageUp:
            if self.spn < 50:
                if self.spn >= 10:
                    self.spn *= 2
                else:
                    self.spn *= 10
                self.search_with_coords(self.CurrentLongitude, self.CurrentLattitude, self.CurrentPoints) 
        elif event.type() == QEvent.KeyPress and event.key() == Qt.Key_Up:
            if self.CurrentLattitude + self.spn < 90:
                self.CurrentLattitude += self.spn
            self.search_with_coords(self.CurrentLongitude, self.CurrentLattitude, self.CurrentPoints) 
        elif event.type() == QEvent.KeyPress and event.key() == Qt.Key_Down:
            if self.CurrentLattitude - self.spn > -90:
                self.CurrentLattitude -= self.spn
            self.search_with_coords(self.CurrentLongitude, self.CurrentLattitude, self.CurrentPoints) 
        elif event.type() == QEvent.KeyPress and event.key() == Qt.Key_Right:
            if self.CurrentLongitude + self.spn < 180:
                self.CurrentLongitude += self.spn
            self.search_with_coords(self.CurrentLongitude, self.CurrentLattitude, self.CurrentPoints) 
        elif event.type() == QEvent.KeyPress and event.key() == Qt.Key_Left:
            if self.CurrentLongitude - self.spn > -180:
                self.CurrentLongitude -= self.spn
            self.search_with_coords(self.CurrentLongitude, self.CurrentLattitude, self.CurrentPoints)
        elif event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
            x, y = event.pos().x(), event.pos().y()
            if x >= 210:
                spnPpix = self.spn / 450
                delta_x = x - 435 
                delta_y = y - 225
                lattitude = delta_y * spnPpix
                longitude = delta_x * spnPpix
                print(f'spnH={spnPpix}')
                print(f'spnW={spnPpix}')
                print(f'delta_x={delta_x}')
                print(f'delta_y={delta_y}')
                print(f'lattitude={lattitude}')
                print(f'longitude={longitude}')
                print(f'CurLong={self.CurrentLongitude}')
                print(f'CurLat={self.CurrentLattitude}')
                print('-------------------')
                self.CurrentLongitude += longitude
                self.CurrentLattitude -= lattitude
                self.search_with_coords(self.CurrentLongitude, self.CurrentLattitude, [f'{self.CurrentLongitude},{self.CurrentLattitude},pm2bll'])
        return QWidget.eventFilter(self, obj, event)
    
    def start_search(self):
        toponym_to_find = self.LELSearch.text()
        if self.search_with_organisation(toponym_to_find) is None:
            self.LELSearch.setText('Ошибка выполнения запроса')
    
    def search_with_coords(self, longitude, lattitude, points=[]):
        self.LELSearch.clearFocus()
        search_params = {
            'll': f'{longitude},{lattitude}',
            'spn': f'{self.spn},{self.spn}',
            'l': self.mapType,
            'size': '450,450',
            'pt':'~'.join(points)
        }

        try:
            response = requests.get(map_server, params=search_params)

            with open(self.map_file, 'wb') as file:
                file.write(response.content)
        
            self.MAP.setPixmap(QPixmap(self.map_file))
            os.remove(self.map_file)
            self.CurrentPoints = points
            return True
        except:
            return None
    
    def search_with_organisation(self, toponym_to_find):
        search_params = {
            'apikey': search_apikey,
            'text': toponym_to_find,
            'lang': 'ru_RU',
        }
        if self.isSearchNearMe:
            search_params['ll'] = ','.join(list(map(str, geocoder.ip('me').latlng[::-1])))

        try:
            response = requests.get(search_server, params=search_params)
            json_response = response.json()
            points = []
            for toponym in json_response['features']:
                points.append(','.join(list(map(str, toponym['geometry']['coordinates']))) + ',pm2bll')
            self.CurrentLongitude = float(points[0].split(',')[0])
            self.CurrentLattitude = float(points[0].split(',')[1])
            self.search_with_coords(self.CurrentLongitude, self.CurrentLattitude, points)
            return True
        except:
            return None

