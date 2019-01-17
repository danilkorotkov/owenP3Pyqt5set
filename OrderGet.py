# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
from PyQt5 import QtCore, QtGui, uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget
from PyQt5.Qt import Qt
import requests
import os
os.environ["DISPLAY"] = ":0" #remote a

MainInterfaceWindow = "order.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(MainInterfaceWindow)


class OrderWindow(QMainWindow, Ui_MainWindow):
    """MainWindow inherits QMainWindow"""

    orders = [['18-000001\nот 25 мая 2019', 0],
              ['28-000001\nот 25 мая 2019', 1],
              ['28-000002\nот 31 мая 2019', 0]]

    def __init__(self, parent=None):
        super(OrderWindow, self).__init__(parent)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        #self.setWindowModality(QtCore.Qt.WindowModal)
        #self.setWindowModality(QtCore.Qt.WindowModal)
        #self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.listWidget.verticalScrollBar().setStyleSheet(_fromUtf8(
            "QScrollBar:vertical {width: 40px; background: rgb(194, 194, 194); margin: 0px;}\n"
            "QScrollBar::handle:vertical {min-height: 40px;}\n"
            "QScrollBar::sub-line:vertical {subcontrol-position: top; subcontrol-origin: margin; height: 70px; }\n"
            "QScrollBar::add-line:vertical {subcontrol-position: bottom; subcontrol-origin: margin; height: 70px; }\n"
            "QScrollBar::down-arrow:vertical, QScrollBar::up-arrow:vertical {background: NONE;}\n"
            "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {background: NONE;}"))

        self.ExitButton.pressed.connect(self.exit)
        self.listWidget.itemDoubleClicked.connect(self.letsgo)

        self.get_orders()
        self.post_orders()
        self.fill_orders()

    def __del__(self):
        self.ui = None

    def exit(self):
        self.close()

    def fill_orders(self):
        """
        заполняем листвиджет списком заказов в работе
        с цветовыми маркерами
        """

        for i in range(len(self.orders)):
            self.listWidget.addItem(self.orders[i][0])
            item = self.listWidget.item(i)
            if self.orders[i][1] == 0:
                item.setBackground(QtGui.QColor("red"))
            else:
                item.setBackground(QtGui.QColor("green"))

    def letsgo(self):
        """
        обработка даблклика на заказе
        :param self:
        :return:
        """
        number = self.orders[self.listWidget.currentRow()][0].replace("\n", " ")[:9]

        item = self.listWidget.item(self.listWidget.currentRow())
        if self.orders[self.listWidget.currentRow()][1] != 0:
            item.setBackground(QtGui.QColor("red"))
            self.orders[self.listWidget.currentRow()][1] = 0
        else:
            item.setBackground(QtGui.QColor("green"))
            self.orders[self.listWidget.currentRow()][1] = 1

        status = self.orders[self.listWidget.currentRow()][1]
        self.statusBar.showMessage('' + number + ' status = ' + str(status))
        print ('' + number + ' status = ' + str(status))

    def get_orders(self):
        """
        GET запрос к 1с серверу
        :return:
        """
        URL = "http://zaborikinovgorod.ru/HTTP_POST/hs/Comagic/v2/IncomingCall"
        PARAMS = {'request': 'getorders'}
        try:
            r = requests.get(url=URL, params=PARAMS)
            data = r.json()
            print(data)
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            print (e)
        except ValueError as e:
            print (e)

    def post_orders(self, number='18-000001', status=1):
        """
        POST запрос к 1с серверу
        :return:
        """
        URL = "http:/zaborikinovgorod.ru/HTTP_POST/hs/Comagic/v2/IncomingCall"
        PARAMS = {'request': 'sendorders',
                  'order': number,
                  'data': status}
        try:
            r = requests.post(url=URL, params=PARAMS)
            answer = r.json()
            print(answer)
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            print (e)
        except ValueError as e:
            print (e)

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)

if __name__ == "__main__":
    # create application
    app = QApplication(sys.argv)
    app.setApplicationName('order check')

    # create widget
    window = OrderWindow()
    window.show()
    # window.showFullScreen()

    # connection
    # QObject.connect(app, SIGNAL('lastWindowClosed()'), app, SLOT('quit()'))

    # execute application
    # sys.exit( app.exec_() )
    app.exec_()
    app.deleteLater()
    sys.exit()