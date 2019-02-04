# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
from PyQt5 import QtCore, QtGui, uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget
from PyQt5.Qt import Qt
import requests
import os
import json
os.environ["DISPLAY"] = ":0" #remote a

MainInterfaceWindow = "order_w.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(MainInterfaceWindow)

class OrderWindow(QMainWindow, Ui_MainWindow):
    orders = []

    def __init__(self, parent=None):
        super(OrderWindow, self).__init__(parent)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowModality(QtCore.Qt.WindowModal)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.listWidget.verticalScrollBar().setStyleSheet(_fromUtf8(
            "QScrollBar:vertical {width: 40px; background: rgb(194, 194, 194); margin: 0px;}\n"
            "QScrollBar::handle:vertical {min-height: 40px;}\n"
            "QScrollBar::sub-line:vertical {subcontrol-position: top; subcontrol-origin: margin; height: 70px; }\n"
            "QScrollBar::add-line:vertical {subcontrol-position: bottom; subcontrol-origin: margin; height: 70px; }\n"
            "QScrollBar::down-arrow:vertical, QScrollBar::up-arrow:vertical {background: NONE;}\n"
            "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {background: NONE;}"))

        self.ExitButton.pressed.connect(self.exit)
        self.listWidget.itemDoubleClicked.connect(self.OrderClick)
        self.RefButton.pressed.connect(self.refresh)

        self.refresh()

    def refresh(self):
       """
       обновить таблицу
       :return:
       """
       self.listWidget.clear()
       self.update()
       self.orders.clear()
       self.statusBar.showMessage('Ищем заказы...')
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
            elif self.orders[i][1] == 1:
                item.setBackground(QtGui.QColor("orange"))

    def ChangeStatus(self, i):
        '''
        смена статуса заказа с отрисовкай в таблице
        '''
        item = self.listWidget.item(i)
        if self.orders[i][1] == 0: # если в работе, то готов
            item.setBackground(QtGui.QColor("green"))
            self.orders[i][1] = 2
        elif self.orders[i][1] == 1: # если в производстве, то готов
            item.setBackground(QtGui.QColor("green"))
            self.orders[i][1] = 2
        elif self.orders[i][1] == 2: # если готов, то возвращаем предыдущий
            self.orders[i][1] = self.orders[i][3]
            if self.orders[i][1] == 0:
                item.setBackground(QtGui.QColor("red"))
            elif self.orders[i][1] == 1:
                item.setBackground(QtGui.QColor("orange"))


    def OrderClick(self):
        """
        обработка даблклика на заказе
        """
        i = self.listWidget.currentRow()
        number = self.orders[i][0].replace("\n", " ")[:11]

        self.statusBar.showMessage('Отправляем изменения заказа ' + number + '...')

        self.ChangeStatus(i)

        status = self.orders[i][1]
        print ('' + number + 'new status = ' + str(status) + ' initial status = ' + str(self.orders[i][3]))

        #URL = 'http://192.168.1.144/TEST/hs/Comagic/v2/updateorder'
        URL = 'http://zaborikinovgorod.ru/TEST/hs/Comagic/v2/updateorder'
        payload = {'GUID': self.orders[i][2], 'status': self.orders[i][3]}
        print('payload= ', payload)

        try:

            response = requests.post(URL, timeout=20, data=payload)
            print('Answer', response.status_code, response.text)

            self.statusBar.showMessage('Отправка прошла успешно')

        except requests.exceptions.RequestException as e:  # This is the correct syntax
            print('Ошибка  1', e)
            self.statusBar.showMessage(str(e))
            self.ChangeStatus(i)
        except ValueError as e:
            print('Ошибка 2', e)
            self.statusBar.showMessage(str(e))
            self.ChangeStatus(i)

    def post_orders(self):
        """
        POST запрос к 1с серверу
        """
        URL = 'http://zaborikinovgorod.ru/TEST/hs/Comagic/v2/orders'
        try:

            response = requests.post(URL, timeout=20)
            datajson = response.json()

            #data = json.load(response.json())
            #print(response.json())

            OrdersList = datajson['orders']

            for i in range(len(OrdersList)):
                self.orders.append([OrdersList[i]['order'],
                                    OrdersList[i]['status'],
                                    OrdersList[i]['GUID'],
                                    OrdersList[i]['status']])

            self.statusBar.showMessage('Получение прошло успешно')

        except requests.exceptions.RequestException as e:  # This is the correct syntax
            print('Ошибка 1', e)
            self.orders.append(['Ошибка\nсоединения', 0])
            self.statusBar.showMessage(str(e))
        except ValueError as e:
            print('Ошибка 2', e)
            self.orders.append(['Пришла\nфигня', 0])
            self.statusBar.showMessage(str(e))

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