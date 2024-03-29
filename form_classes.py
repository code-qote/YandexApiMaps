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
        self.search_with_coords(self.CurrentLongitude, self.CurrentLattitude, self.CurrentToponyms, self.CurrentRoute)

    def deletePoint(self):
        self.isPoint = False
        self.CurrentPoint = None
        self.LELSearch.clear()
        self.TWToponyms.clear()
        self.LEStart.clear()
        self.LEFinish.clear()
        self.RBSearchNearMe.setChecked(False)
        self.search_with_coords(self.CurrentLongitude, self.CurrentLattitude, self.isPoint)
    
    def updateSearch(self): 
        self.isSearchNearMe = not(self.isSearchNearMe)

    def config(self):
        self.BSearch.clicked.connect(self.start_search)
        self.BCancel.clicked.connect(self.deletePoint)
        self.BSearch.setAutoDefault(True)
        self.BRoute.clicked.connect(self.start_route)
        self.isSearchNearMe = False
        self.RBSearchNearMe.toggled.connect(self.updateSearch)
        self.LELSearch.returnPressed.connect(self.BSearch.click)
        self.TWToponyms.currentChanged.connect(self.tabclick)
        self.CurrentToponyms = []
        self.CurrentRoute = ''
        self.tabs = []
        self.spn_y = 0.0015
        self.spn_x = 0.0025
        self.z = 17
        self.lock_z = False
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
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_PageDown and not self.lock_z:
            if self.z < 17:
                self.z += 1
                self.spn_x /= 2
                self.spn_y /= 2
                self.search_with_coords(self.CurrentLongitude, self.CurrentLattitude, self.CurrentToponyms, self.CurrentRoute) 
        elif event.type() == QEvent.KeyPress and event.key() == Qt.Key_PageUp and not self.lock_z:
            if self.z > 0:
                self.z -= 1
                self.spn_x *= 2
                self.spn_y *= 2
                self.search_with_coords(self.CurrentLongitude, self.CurrentLattitude, self.CurrentToponyms, self.CurrentRoute)
        elif event.type() == QEvent.KeyPress and event.key() == Qt.Key_Up:
            if self.CurrentLattitude + self.spn_y < 90:
                self.CurrentLattitude += self.spn_y
                self.search_with_coords(self.CurrentLongitude, self.CurrentLattitude, self.CurrentToponyms, self.CurrentRoute) 
        elif event.type() == QEvent.KeyPress and event.key() == Qt.Key_Down:
            if self.CurrentLattitude - self.spn_y > -90:
                self.CurrentLattitude -= self.spn_y
                self.search_with_coords(self.CurrentLongitude, self.CurrentLattitude, self.CurrentToponyms, self.CurrentRoute) 
        elif event.type() == QEvent.KeyPress and event.key() == Qt.Key_Right:
            if self.CurrentLongitude + self.spn_x < 180:
                self.CurrentLongitude += self.spn_x
                self.search_with_coords(self.CurrentLongitude, self.CurrentLattitude, self.CurrentToponyms, self.CurrentRoute) 
        elif event.type() == QEvent.KeyPress and event.key() == Qt.Key_Left:
            if self.CurrentLongitude - self.spn_x > -180:
                self.CurrentLongitude -= self.spn_x
                self.search_with_coords(self.CurrentLongitude, self.CurrentLattitude, self.CurrentToponyms, self.CurrentRoute)
        return QWidget.eventFilter(self, obj, event)

    def start_search(self):
        toponym_to_find = self.LELSearch.text()
        if self.search_with_organisation(toponym_to_find) is None:
            self.LELSearch.setText('Ошибка выполнения запроса')
    
    def start_route(self):
        start = self.LEStart.text()
        finish = self.LEFinish.text()
        start_coords = self.get_coords(start)
        finish_coords = self.get_coords(finish)
        if start_coords and finish_coords:
            self.LELSearch.clear()
            self.RBSearchNearMe.setChecked(False)
            self.search_route(start_coords, finish_coords)
    
    def get_coords(self, toponym_to_find):
        search_params = {
            'apikey': search_apikey,
            'text': toponym_to_find,
            'lang': 'ru_RU',
        }
        
        try:
            response = requests.get(search_server, params=search_params)
            json_response = response.json()
            toponym = json_response['features'][0]
            return toponym['geometry']['coordinates']
        except:
            return None
    
    def tabclick(self, i):
        for tab in self.tabs:
            if tab['number'] == i:
                self.search_with_coords(tab['coords'][0], tab['coords'][1], self.CurrentToponyms)
                break
    
    def search_route(self, start, finish):
        response = requests.get(route_server + f'{start[0]},{start[1]};{finish[0]},{finish[1]}', params=route_params)
        json_response = response.json()
        coordinates = json_response['routes'][0]['geometry']['coordinates']
        distance = round(json_response['routes'][0]['legs'][0]['distance'] / 1000, 1)
        duration = round(json_response['routes'][0]['legs'][0]['duration'])
        hours = duration // 3600
        minutes = (duration % 3600) // 60

        self.TWToponyms.clear()
        tab = QWidget()
        textEdit = QTextEdit(tab)
        textEdit.setGeometry(QRect(0, -10, 171, 461))
        textEdit.setReadOnly(True)
        text = f'\nРасстояние: {distance} км\nВремя: {hours} ч {minutes} мин'
        textEdit.setPlainText(text)
        self.TWToponyms.addTab(tab, '')

        pl = ''
        for coord in coordinates:
            pl += f'{coord[0]},{coord[1]},'
        self.lock_z = True
        self.z = 16
        self.spn_y = 0.003
        self.spn_x = 0.005
        self.search_with_coords(start[0], start[1], [], pl[:-1])
        

    def search_with_coords(self, longitude, lattitude, toponyms=[], pl=None):
        self.LELSearch.clearFocus()
        self.LEStart.clearFocus()
        self.LEFinish.clearFocus()
        if toponyms is not False:
            points = [toponym['point'] for toponym in toponyms]
        else:
            points = []
        if pl is not None:
            points.append(f'{pl.split(",")[0]},{pl.split(",")[1]},pm2al~{pl.split(",")[-2]},{pl.split(",")[-1]},pm2bl')
        search_params = {
            'll': f'{longitude},{lattitude}',
            'z': f'{self.z}',
            'l': self.mapType,
            'size': '450,450',
            'pt':'~'.join(points)
        }
        if pl is not None:
            pl_ = pl.split(',')
            new = []
            k = 0
            for i in range(len(pl_) - 1):
                if ((longitude - 3 * self.spn_x <= float(pl_[i]) <= longitude + 3 * self.spn_x) or (lattitude - 3 * self.spn_y <= float(pl_[i + 1]) <= lattitude + 3 * self.spn_y)) and k < 100:
                    new.append(pl_[i])
                    new.append(pl_[i + 1])
                    k += 1
            if new:
                search_params['pl'] = ','.join(new)

        try:
            response = requests.get(map_server, params=search_params)

            with open(self.map_file, 'wb') as file:
                file.write(response.content)
        
            self.MAP.setPixmap(QPixmap(self.map_file))
            os.remove(self.map_file)

            self.CurrentToponyms = toponyms
            self.CurrentLongitude = float(longitude)
            self.CurrentLattitude = float(lattitude)
            self.CurrentRoute = pl
            return True
        except:
            return None
    
    def search_with_organisation(self, toponym_to_find, solo=False):
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
            toponyms = []
            for toponym in json_response['features']:
                point = ','.join(list(map(str, toponym['geometry']['coordinates']))) + ',pm2bll'
                try:
                    metadata = toponym['properties']['CompanyMetaData']
                    org = True
                except KeyError:
                    metadata = toponym['properties']['GeocoderMetaData']
                    org = False
                if org:
                    name = metadata['name']
                    address = metadata['address']
                    url = metadata['url']
                    phones = [phone['formatted'] for phone in metadata['Phones']]              
                    hours = metadata['Hours']['text']
                    toponyms.append(
                        {
                         'org':True,
                         'name':name,
                         'address':address,
                         'url':url,
                         'phones':phones,
                         'hours':hours,
                         'point': point
                        })
                else:
                    text = metadata['text']
                    toponyms.append(
                        {
                         'org':False,
                         'text':text,
                         'point': point
                        })
            self.CurrentToponyms = toponyms
            firstPoint = toponyms[0]['point'].split(',')
            self.CurrentLongitude = float(firstPoint[0])
            self.CurrentLattitude = float(firstPoint[1])
            if solo:
                self.CurrentToponyms = [self.CurrentToponyms[0]]
            
            self.tabs = []
            self.TWToponyms.clear()

            i = 0
            for toponym in toponyms:
                tab = QWidget()
                textEdit = QTextEdit(tab)
                textEdit.setGeometry(QRect(0, -10, 171, 461))
                textEdit.setReadOnly(True)
                if toponym['org']:
                    p = '\n'.join(toponym['phones'])
                    text = f'''\n{toponym['name']}\nАдрес:\n{toponym['address']}\nВремя работы:\n{toponym['hours']}\nТелефоны:\n{p}\nСайт\n{toponym['url']}'''
                else:
                    text = f'''\n{toponym['text']}'''
                coords = toponym['point'].split(',')[:2]
                self.tabs.append({
                    'number': i,
                    'coords': coords
                }) 
                textEdit.setPlainText(text)
                self.TWToponyms.addTab(tab, '')
                i += 1
            self.lock_z = False
            self.LEStart.clear()
            self.LEFinish.clear()
            self.search_with_coords(self.CurrentLongitude, self.CurrentLattitude, self.CurrentToponyms)
            return True
        except:
            return None
