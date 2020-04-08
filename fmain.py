# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fmain.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_fmain(object):
    def setupUi(self, fmain):
        fmain.setObjectName("fmain")
        fmain.resize(660, 450)
        self.centralwidget = QtWidgets.QWidget(fmain)
        self.centralwidget.setObjectName("centralwidget")
        self.MAP = QtWidgets.QLabel(self.centralwidget)
        self.MAP.setGeometry(QtCore.QRect(210, 0, 450, 450))
        self.MAP.setText("")
        self.MAP.setObjectName("MAP")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 0, 111, 16))
        self.label_2.setObjectName("label_2")
        self.BSearch = QtWidgets.QPushButton(self.centralwidget)
        self.BSearch.setGeometry(QtCore.QRect(10, 420, 75, 23))
        self.BSearch.setFocusPolicy(QtCore.Qt.NoFocus)
        self.BSearch.setObjectName("BSearch")
        self.BMap = QtWidgets.QPushButton(self.centralwidget)
        self.BMap.setGeometry(QtCore.QRect(10, 80, 75, 23))
        self.BMap.setFocusPolicy(QtCore.Qt.NoFocus)
        self.BMap.setObjectName("BMap")
        self.BSat = QtWidgets.QPushButton(self.centralwidget)
        self.BSat.setGeometry(QtCore.QRect(10, 110, 75, 23))
        self.BSat.setFocusPolicy(QtCore.Qt.NoFocus)
        self.BSat.setObjectName("BSat")
        self.BSkl = QtWidgets.QPushButton(self.centralwidget)
        self.BSkl.setGeometry(QtCore.QRect(10, 140, 75, 23))
        self.BSkl.setFocusPolicy(QtCore.Qt.NoFocus)
        self.BSkl.setObjectName("BSkl")
        self.LELSearch = QtWidgets.QLineEdit(self.centralwidget)
        self.LELSearch.setGeometry(QtCore.QRect(10, 20, 191, 20))
        self.LELSearch.setMouseTracking(True)
        self.LELSearch.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.LELSearch.setObjectName("LELSearch")
        self.BCancel = QtWidgets.QPushButton(self.centralwidget)
        self.BCancel.setGeometry(QtCore.QRect(10, 390, 75, 23))
        self.BCancel.setFocusPolicy(QtCore.Qt.NoFocus)
        self.BCancel.setObjectName("BCancel")
        self.RBSearchNearMe = QtWidgets.QRadioButton(self.centralwidget)
        self.RBSearchNearMe.setGeometry(QtCore.QRect(10, 50, 121, 17))
        self.RBSearchNearMe.setFocusPolicy(QtCore.Qt.NoFocus)
        self.RBSearchNearMe.setObjectName("RBSearchNearMe")
        fmain.setCentralWidget(self.centralwidget)

        self.retranslateUi(fmain)
        QtCore.QMetaObject.connectSlotsByName(fmain)

    def retranslateUi(self, fmain):
        _translate = QtCore.QCoreApplication.translate
        fmain.setWindowTitle(_translate("fmain", "Maps"))
        self.label_2.setText(_translate("fmain", "Введите запрос"))
        self.BSearch.setText(_translate("fmain", "Поиск"))
        self.BMap.setText(_translate("fmain", "Карта"))
        self.BSat.setText(_translate("fmain", "Спутник"))
        self.BSkl.setText(_translate("fmain", "Гибрид"))
        self.BCancel.setText(_translate("fmain", "Сброс"))
        self.RBSearchNearMe.setText(_translate("fmain", "Искать около меня"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    fmain = QtWidgets.QMainWindow()
    ui = Ui_fmain()
    ui.setupUi(fmain)
    fmain.show()
    sys.exit(app.exec_())
