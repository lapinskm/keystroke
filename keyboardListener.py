#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import QDateTime

import recorderUi

class Main:

   def log_key(self, key, isUp):
      date = QDateTime.currentMSecsSinceEpoch()
      logText=str(date)+":"+str(key.key())+"("+ key.text()+") "
      if isUp:
         logText=logText+"pressed"
      else:
         logText=logText+"released"
      self.ui.logDisplay.append(logText)
      print logText


   def on_keydown(self, key):
      self.log_key(key, True)

   def on_keyup(self, key):
      self.log_key(key, False)

   def __init__(self):
      # Create an PyQT4 application object.
     self.app = QApplication(sys.argv)

     # The QWidget widget is the base class of all user interface objects in PyQt4.
     self.widget = QWidget()
     # Create ui
     self.ui = recorderUi.Ui_MainWindow()
     self.ui.setupUi(self.widget)

     self.widget.keyPressEvent   = self.on_keydown
     self.widget.keyReleaseEvent = self.on_keyup
   
   def run(self):
     # Show window
     self.widget.show()
     sys.exit(self.app.exec_())

Main().run();
