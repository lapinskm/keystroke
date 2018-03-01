#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import QDateTime


def on_key(key):
   print "### KEY text: " + key.text()
   print  key.key()
   print  QDateTime.currentMSecsSinceEpoch()

def on_keydown(key):
   print "############# key pressed  ###";
   on_key(key)

def on_keyup(key):
   print "############# key released ###";
   on_key(key)


# Create an PyQT4 application object.
a = QApplication(sys.argv)

# The QWidget widget is the base class of all user interface objects in PyQt4.
w = QWidget()


# Set window size.
w.resize(320, 240)


w.setWindowTitle("key stroke recorder")
w.keyPressEvent=on_keydown
w.keyReleaseEvent=on_keyup

# Show window
w.show()

sys.exit(a.exec_())
