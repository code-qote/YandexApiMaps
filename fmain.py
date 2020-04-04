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
        fmain.resize(813, 489)
        self.centralwidget = QtWidgets.QWidget(fmain)
        self.centralwidget.setObjectName("centralwidget")
        self.MAP = QtWidgets.QLabel(self.centralwidget)
        self.MAP.setGeometry(QtCore.QRect(150, 0, 661, 491))
        self.MAP.setText("")
        self.MAP.setObjectName("MAP")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 10, 47, 13))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 50, 47, 13))
        self.label_3.setObjectName("label_3")
        self.LELongitude = QtWidgets.QLineEdit(self.centralwidget)
        self.LELongitude.setEnabled(True)
        self.LELongitude.setGeometry(QtCore.QRect(10, 30, 61, 20))
        self.LELongitude.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.LELongitude.setObjectName("LELongitude")
        self.LELattitude = QtWidgets.QLineEdit(self.centralwidget)
        self.LELattitude.setGeometry(QtCore.QRect(10, 70, 61, 20))
        self.LELattitude.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.LELattitude.setObjectName("LELattitude")
        self.BSearch = QtWidgets.QPushButton(self.centralwidget)
        self.BSearch.setGeometry(QtCore.QRect(10, 460, 75, 23))
        self.BSearch.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.BSearch.setObjectName("BSearch")
        fmain.setCentralWidget(self.centralwidget)

        self.retranslateUi(fmain)
        QtCore.QMetaObject.connectSlotsByName(fmain)

    def retranslateUi(self, fmain):
        _translate = QtCore.QCoreApplication.translate
        fmain.setWindowTitle(_translate("fmain", "Maps"))
        self.label_2.setText(_translate("fmain", "Долгота"))
        self.label_3.setText(_translate("fmain", "Широта"))
        self.BSearch.setText(_translate("fmain", "Поиск"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    fmain = QtWidgets.QMainWindow()
    ui = Ui_fmain()
    ui.setupUi(fmain)
    fmain.show()
    sys.exit(app.exec_())
