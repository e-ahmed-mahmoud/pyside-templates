#!/usr/bin/env python3
#
#   splash.py
#   An example subclass of QSplashScreen to be implemented inside a MainWindow object.
#   Using Python 3.6 and PySide2 v.5.12
#
#   Copyright (C) 2019 Robert Parker
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program. If not, see <https://www.gnu.org/licenses/>.


import time
from PySide2.QtCore import Qt
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QSplashScreen, QVBoxLayout, QProgressBar, QLabel, QDesktopWidget


class Splash(QSplashScreen):
    def __init__(self, image, width=400, height=300):
        """
        Subclass of QSplashScreen that appears as the program loads. It sets up a background image,
        and includes a loading_update() method to update the loading progress bar and message.
        
        :image: str, file path to background image
        :width: int, specified width for splash screen
        :height: in, specified height for splash screen
        """
        super().__init__()
        self.width, self.height = width, height
        self.setFixedSize(self.width, self.height)
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        self.setPixmap(QPixmap(image).scaled(width, height))
        self.setup()
        self.time_start = time.clock()
        

    def loading_update(self, percent, message):
        """
        Call this method to tell the splash screen to update the prgoress bar and loading message.
        
        :percent: int, percent of loading to show on progress bar
        :message: str, message to accompany progress bar, e.g. "Loading data"
        """
        
        self.message_display.setText(message)
        if percent == 100:
            seconds = time.clock()
            while seconds < 2.5:  # This sets the minimum time the splash screen should be shown
                time.sleep(0.5)
                seconds = time.clock()
                status = round(seconds * 40, 0)  # Multiplier must be 100 divided by minimum time set above
                self.bar.setValue(status)
            self.hide()
        else:
            seconds = time.clock()
            status = min(percent, round(seconds * 40, 0))
            self.bar.setValue(status)

    def setup(self):
        """Sets up the layout of the splash screen"""
        
        # Window
        self.layout = QVBoxLayout(self)

        # Progress bar
        self.bar = QProgressBar()
        self.bar.setMinimum(0)
        self.bar.setMaximum(100)
        self.bar.setTextVisible(False)
        self.layout.addStretch(1)
        self.layout.addWidget(self.bar)

        # Message
        self.message_display = QLabel(text="Loading...")  # Change starting message as desired
        self.layout.addWidget(self.message_display)

        self.centre_on_screen()

    def centre_on_screen(self):
        """Centers the splash screen on the desktop"""
        
        centre = QDesktopWidget().availableGeometry().center()
        x, y = centre.x() - self.width / 2, centre.y() - self.height / 2
        x = 0 if x < 0 else x
        y = 0 if y < 0 else y
        self.move(x, y)
