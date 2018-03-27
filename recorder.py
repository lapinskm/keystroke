#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import QDateTime
from PyQt4.QtCore import QTimer

import recorderUi

class Main:

   def on_start_stop(self):
      if not self.running:
         self.running=True
         self.start_recording()
      else:
         self.running=False
         self.stop_recording()

   def start_recording(self):
      self.log_text("recording started")
      self.timer.start(1000)
      self.ui.timeDisplay.display(0)
      self.ui.startStopButton.setText("Stop recording")
      self.elapsedTime=0

   def stop_recording(self):
      self.log_text("recording stopped")
      self.ui.startStopButton.setText("Start recording")
      self.timer.stop()

   def update_timer(self):
      self.elapsedTime = self.elapsedTime + 1
      self.ui.timeDisplay.display (self.elapsedTime)

   def log_text(self, text):
      self.ui.logDisplay.append(text)
      print text

   def log_key(self, key, isUp):
      if not self.running:
         return
      date = QDateTime.currentMSecsSinceEpoch()
      logText=str(date)+":"+str(key.key())+"("+ key.text()+") "
      if isUp:
         logText=logText+"pressed"
      else:
         logText=logText+"released"
      self.log_text(logText)

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
     # Elapsed Time counter
     self.timer = QTimer()
     self.timer.timeout.connect(self.update_timer)
     self.elapsedTime=0

     self.ui.startStopButton.clicked.connect(self.on_start_stop)
     self.running=False

     self.widget.keyPressEvent = self.on_keydown
     self.widget.keyReleaseEvent = self.on_keyup
   
   def run(self):
     # Show window
     self.widget.show()
     sys.exit(self.app.exec_())

Main().run();
