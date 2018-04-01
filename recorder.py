#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#

import csv
import pyaudio
import sys
import wave


from PyQt5.QtCore import QDateTime
from PyQt5.QtCore import QTimer

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QWidget


import recorderUi

#Audio recorder constants
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 8192

class Main:

   def on_start_stop(self):
      if not self.running and self.files_are_set():
         self.running=True
         self.start_recording()
      elif self.running:
         self.running=False
         self.stop_recording()
      elif not self.files_are_set():
         self.log_text("Files are not set!")

   def files_are_set(self):
      return self.keyFileName and self.audioFileName

   def on_browse_key_file(self):
      self.keyFileName = QFileDialog.getSaveFileName(self.widget,
                     "Choose a path and filename of key data",
                     "data.csv", filter = "text data files (*.csv)")[0]
      self.ui.keyRecordingFileEdit.setText(self.keyFileName)

   def on_browse_audio_file(self):
      self.audioFileName = QFileDialog.getSaveFileName(self.widget,
                     "Choose a path and filename of audio data",
                     "data.wav", filter = "audio files (*.wav)")[0]
      self.ui.audioRecordingFileEdit.setText(self.audioFileName)

   def start_recording(self):
      self.log_text("recording started")

      #ui behaviour
      self.uiTimer.start()
      self.ui.timeDisplay.display(0)
      self.ui.startStopButton.setText("Stop recording")
      self.elapsedTime = 0
      self.ui.keyRecordingFileBrowseButton.setDisabled(True)
      self.ui.audioRecordingFileBrowseButton.setDisabled(True)

      #key recording
      assert self.keyFileName
      self.keyFile = open(self.keyFileName, "w")
      self.log_text("key input data will be saved to " + self.keyFileName)
      csv.writer(self.keyFile).writerow(("timestamp", "key_code", "up_or_down"))
      self.startTime = QDateTime.currentMSecsSinceEpoch()
      #audio recording
      assert self.audioFileName
      self.log_text("audio input data will be saved to " + self.audioFileName)
      self.audioStream = self.audioApi.open(format=FORMAT, channels=CHANNELS,
                                            rate=RATE, input=True,
                                            frames_per_buffer=CHUNK)
      self.audioFile = wave.open(self.audioFileName, 'wb')
      self.audioFile.setnchannels(CHANNELS)
      self.audioFile.setsampwidth(self.audioApi.get_sample_size(FORMAT))
      self.audioFile.setframerate(RATE)
      self.audioRecorderTimer.start()

   def on_record_audio_timer(self):
      assert self.running
      data = self.audioStream.read(CHUNK)
      self.audioFile.writeframes(b''.join([data]))

   def stop_recording(self):
      #ui behaviour
      self.log_text("recording stopped")
      self.ui.startStopButton.setText("Start recording")
      self.uiTimer.stop()
      self.ui.keyRecordingFileBrowseButton.setDisabled(False)
      self.ui.audioRecordingFileBrowseButton.setDisabled(False)

      #key recording
      assert self.keyFile
      self.keyFile.close()
      self.log_text("key input data is saved to " + self.keyFileName)
      self.startTime = 0

      #audio recording
      self.audioRecorderTimer.stop()
      assert self.audioFileName
      self.audioStream.stop_stream()
      self.audioStream.close()
      self.audioFile.close()
      self.log_text("audio input data is saved to " + self.audioFileName)


   def update_ui_timer(self):
      self.elapsedTime = self.elapsedTime + 1
      self.ui.timeDisplay.display (self.elapsedTime)

   def log_text(self, text):
      self.ui.logDisplay.append(text)
      print(text)

   def log_key(self, key, isUp):
      if not self.running:
         return
      assert self.startTime
      time = QDateTime.currentMSecsSinceEpoch() - self.startTime
      logText = str(time) + ":" + str(key.key()) + "(" + key.text() + ") "
      if isUp:
         logText = logText + "pressed"
      else:
         logText = logText + "released"
      self.log_text(logText)
      assert self.keyFile
      csv.writer(self.keyFile).writerow((time, key.key(), "up" if isUp else "down"))
      

   def on_keydown(self, key):
      self.log_key(key, True)

   def on_keyup(self, key):
      self.log_key(key, False)

   def __init__(self):
      # Create an PyQT4 application object.
      self.app = QApplication(sys.argv)

      # Create ui
      self.widget = QWidget()
      self.ui = recorderUi.Ui_MainWindow()
      self.ui.setupUi(self.widget)

      # Elapsed Time counter
      self.uiTimer = QTimer()
      self.uiTimer.timeout.connect(self.update_ui_timer)
      self.uiTimer.setInterval(1000)
      self.elapsedTime = 0

      #start/stop button
      self.ui.startStopButton.clicked.connect(self.on_start_stop)
      self.running = False

      #browse files buttons
      self.keyFileName = ""
      self.audioFileName = ""
      self.ui.keyRecordingFileBrowseButton.clicked.connect(self.on_browse_key_file)
      self.ui.audioRecordingFileBrowseButton.clicked.connect(self.on_browse_audio_file)

      self.keyFile = None
      self.startTime = 0

      # Audio recording setup
      self.audioApi = pyaudio.PyAudio()
      self.audioRecorderTimer = QTimer()
      self.audioRecorderTimer.setInterval(0)
      self.audioRecorderTimer.timeout.connect(self.on_record_audio_timer)

      # Capture key input of widget
      self.widget.keyPressEvent = self.on_keydown
      self.widget.keyReleaseEvent = self.on_keyup
   
   def run(self):
      # Show window
      self.widget.show()
      sys.exit(self.app.exec_())
      self.audioApi.terminate()

Main().run();
