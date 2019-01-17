#!/usr/bin/python3
# -*- coding: utf-8 -*-
#python3 -c "from PyQt5.QtCore import QT_VERSION_STR;from PyQt5.Qt import PYQT_VERSION_STR;from sip import SIP_VERSION_STR;print('Qt version: ',QT_VERSION_STR);print('SIP version: ',SIP_VERSION_STR);print('PyQt version: ',PYQT_VERSION_STR)"

import sys

# import PyQt4 QtCore and QtGui modules
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QMainWindow, QApplication
import os
os.environ["DISPLAY"] = ":0" #remote a

from mainwindow import MainWindow

if __name__ == '__main__':

    # create application
    app = QApplication( sys.argv )
    app.setApplicationName( 'owen control' )

    # create widget
    window = MainWindow()
    #window.show()
    window.showFullScreen()  

    # connection
    #QObject.connect( app, SIGNAL( 'lastWindowClosed()' ), app, SLOT( 'quit()' ) )
    app.lastWindowClosed.connect(quit)

    # execute application
    #sys.exit( app.exec_() )
    app.exec_()
    app.deleteLater()
    sys.exit()    
