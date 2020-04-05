from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from fmain import Ui_fmain
from consts import *
import requests
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
        self.search_with_coords(self.CurrentLongitude, self.CurrentLattitude, self.isPoint)

    def deletePoint(self):
        self.isPoint = False
        self.CurrentPoint = None
        self.LELSearch.clear()
        self.LEAddress.clear()
        self.search_with_coords(self.CurrentLongitude, self.CurrentLattitude, self.isPoint)

    def config(self):
        self.BSearch.clicked.connect(self.start_search)
        self.BCancel.clicked.connect(self.deletePoint)
        self.BSearch.setAutoDefault(True)
        self.LELSearch.returnPressed.connect(self.BSearch.click)
        self.spn = 0.01
        self.isPoint = False
        self.CurrentPoint = None
        self.installEventFilter(self)
        self.CurrentLattitude = 53.2
        self.CurrentLongitude = 50.15
        self.mapType = 'map'
        self.map_file = 'map.png'
        self.BMap.clicked.connect(partial(self.updateMapType, Mtype='map', map_file='map.png'))
        self.BSat.clicked.connect(partial(self.updateMapType, Mtype='sat', map_file='map.jpg'))
        self.BSkl.clicked.connect(partial(self.updateMapType, Mtype='sat,skl', map_file='map.jpg'))
        self.search_with_coords(self.CurrentLongitude, self.CurrentLattitude, False)
    
    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_PageDown:
            if self.spn > 0.0001:
                self.spn /= 10
                self.search_with_coords(self.CurrentLongitude, self.CurrentLattitude, self.isPoint) 
        elif event.type() == QEvent.KeyPress and event.key() == Qt.Key_PageUp:
            if self.spn < 50:
                if self.spn >= 10:
                    self.spn *= 2
                else:
                    self.spn *= 10
                self.search_with_coords(self.CurrentLongitude, self.CurrentLattitude, self.isPoint)
        elif event.type() == QEvent.KeyPress and event.key() == Qt.Key_Up:
            if self.CurrentLattitude + self.spn < 90:
                self.CurrentLattitude += self.spn
            self.search_with_coords(self.CurrentLongitude, self.CurrentLattitude, self.isPoint)
        elif event.type() == QEvent.KeyPress and event.key() == Qt.Key_Down:
            if self.CurrentLattitude - self.spn > -90:
                self.CurrentLattitude -= self.spn
            self.search_with_coords(self.CurrentLongitude, self.CurrentLattitude, self.isPoint)
        elif event.type() == QEvent.KeyPress and event.key() == Qt.Key_Right:
            if self.CurrentLongitude + self.spn < 180:
                self.CurrentLongitude += self.spn
            self.search_with_coords(self.CurrentLongitude, self.CurrentLattitude, self.isPoint)
        elif event.type() == QEvent.KeyPress and event.key() == Qt.Key_Left:
            if self.CurrentLongitude - self.spn > -180:
                self.CurrentLongitude -= self.spn
            self.search_with_coords(self.CurrentLongitude, self.CurrentLattitude, self.isPoint)
        return QWidget.eventFilter(self, obj, event)
    
    def start_search(self):
        toponym_to_find = self.LELSearch.text()
        if self.search_with_toponym(toponym_to_find) is None:
            self.LELSearch.setText('Ошибка выполнения запроса')
    
    def search_with_coords(self, longitude, lattitude, point=True, new_point=False):
        self.LELSearch.clearFocus()
        search_params = {
            'll': f'{longitude},{lattitude}',
            'spn': f'{self.spn},{self.spn}',
            'l': self.mapType,
        }
        if point and not new_point:
            search_params['pt'] = self.CurrentPoint
        elif point and new_point:
            self.CurrentPoint =  f'{longitude},{lattitude},pm2bll'
            search_params['pt'] = self.CurrentPoint
        else:
            self.CurrentPoint = None
        self.isPoint = point

        try:
            response = requests.get(map_server, params=search_params)

            with open(self.map_file, 'wb') as file:
                file.write(response.content)
        
            self.MAP.setPixmap(QPixmap(self.map_file))
            return True
        except:
            return None
    
    def search_with_toponym(self, geocode):
        search_params = {
            'geocode': geocode,
            'apikey': geocoder_apikey,
            'format': 'json'
        }
        
        try:
            response = requests.get(geocoder_server, params=search_params)
            json_response = response.json()

            toponym = json_response['response']['GeoObjectCollection']['featureMember'][0]
            toponym_address = toponym['GeoObject']['metaDataProperty']['GeocoderMetaData']['text']
            self.CurrentLongitude, self.CurrentLattitude = map(float, toponym['GeoObject']['Point']['pos'].split())
            self.LEAddress.setText(toponym_address)
            self.search_with_coords(self.CurrentLongitude, self.CurrentLattitude, True, True)
            return True
        except:
            return None
