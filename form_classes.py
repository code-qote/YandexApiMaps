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
        self.LEAddress.clear()
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
            if self.z < 17:
                self.z += 1
                self.spn_x /= 2
                self.spn_y /= 2
                self.search_with_coords(self.CurrentLongitude, self.CurrentLattitude, self.CurrentToponyms, self.CurrentRoute) 
        elif event.type() == QEvent.KeyPress and event.key() == Qt.Key_PageUp:
            if self.z > 0:
                self.z -= 1
                self.spn_x *= 2
                self.spn_y *= 2
                self.search_with_coords(self.CurrentLongitude, self.CurrentLattitude, self.CurrentToponyms, self.CurrentRoute)
        elif event.type() == QEvent.KeyPress and event.key() == Qt.Key_Up:
            if self.CurrentLattitude + self.spn < 90:
                self.CurrentLattitude += self.spn
                self.search_with_coords(self.CurrentLongitude, self.CurrentLattitude, self.CurrentToponyms, self.CurrentRoute) 
        elif event.type() == QEvent.KeyPress and event.key() == Qt.Key_Down:
            if self.CurrentLattitude - self.spn > -90:
                self.CurrentLattitude -= self.spn
                self.search_with_coords(self.CurrentLongitude, self.CurrentLattitude, self.CurrentToponyms, self.CurrentRoute) 
        elif event.type() == QEvent.KeyPress and event.key() == Qt.Key_Right:
            if self.CurrentLongitude + self.spn < 180:
                self.CurrentLongitude += self.spn
                self.search_with_coords(self.CurrentLongitude, self.CurrentLattitude, self.CurrentToponyms, self.CurrentRoute) 
        elif event.type() == QEvent.KeyPress and event.key() == Qt.Key_Left:
            if self.CurrentLongitude - self.spn > -180:
                self.CurrentLongitude -= self.spn
                self.search_with_coords(self.CurrentLongitude, self.CurrentLattitude, self.CurrentToponyms, self.CurrentRoute)
        elif event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
            x, y = event.pos().x(), event.pos().y()
            if x >= 210 and x < 670:
                import math
                from haversine import haversine, Unit
                #spnPpix = self.spn / 450
                print(f'центр{self.CurrentLattitude},{self.CurrentLongitude}')
                print(f'право{self.CurrentLattitude + self.spn_y},{self.CurrentLongitude}')
                m_y = haversine((self.CurrentLattitude, self.CurrentLongitude), (self.CurrentLattitude + self.spn_y, self.CurrentLongitude)) * 1000
                m_x = haversine((self.CurrentLattitude, self.CurrentLongitude), (self.CurrentLattitude, self.CurrentLongitude + self.spn_x)) * 1000
                m_y /= 225
                m_x /= 225
                delta_x = (x - 435) * m_x
                delta_y = (y - 225) * m_y
                #lattitude = delta_y * spnPpix
                #longitude = delta_x * spnPpix
                #print(f'spnH={spnPpix}')
                #print(f'spnW={spnPpix}')
                #print(f'delta_x={delta_x}')
                #print(f'delta_y={delta_y}')
                #print(f'lattitude={lattitude}')
                #print(f'longitude={longitude}')
                ##print(f'CurLong={self.CurrentLongitude}')
                #print(f'CurLat={self.CurrentLattitude}')
                #print(f'spn={self.spn}')
                #print('-------------------')
                r = 6372795
                #print(2 * r * math.asin(math.cos(self.CurrentLattitude* math.pi / 180)*math.sin(self.spn* math.pi / 180 / 4)))
                #print(self.spn)
                longitude = 2*math.asin(math.sin(delta_x / 2 * r)/math.cos(self.CurrentLattitude)) + self.CurrentLongitude
                lattitude = 2*math.asin(math.sin(delta_y / 2 * r)) + self.CurrentLattitude
                self.CurrentLongitude = longitude
                self.CurrentLattitude = lattitude
                self.search_with_organisation(f'{self.CurrentLongitude},{self.CurrentLattitude}', True)
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
        pl = ''
        for coord in coordinates:
            pl += f'{coord[0]},{coord[1]},'
        self.search_with_coords(start[0], start[1], [], pl[:-1])
        

    def search_with_coords(self, longitude, lattitude, toponyms=[], pl=None):
        self.LELSearch.clearFocus()
        self.LEStart.clearFocus()
        self.LEFinish.clearFocus()
        points = [toponym['point'] for toponym in toponyms]
        #points.append(f'{longitude + self.spn_x},{lattitude},pm2bll')
        #points.append(f'{longitude - self.spn_x},{lattitude},pm2bll')
        #points.append(f'{longitude},{lattitude + self.spn_x},pm2bll')
        #points.append(f'{longitude},{lattitude - self.spn_y},pm2bll')
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
            for i in range(len(pl_)):
                if (i + 1) % 2 != 0:
                    if longitude - self.spn_x <= float(pl_[i]) <= longitude + self.spn_x:
                        new.append(pl_[i])
                    else:
                        break
                else:
                    if lattitude - self.spn_y <= float(pl_[i]) <= lattitude + self.spn_y:
                        new.append(pl_[i])
                    else:
                        break
            if new:
                search_params['pl'] = ','.join(new)

        try:
            response = requests.get(map_server, params=search_params)
            print(response.request.url)

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
            
            self.search_with_coords(self.CurrentLongitude, self.CurrentLattitude, self.CurrentToponyms)
            return True
        except:
            return None
