import time
from PySide2.QtCore import Qt
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QSplashScreen, QVBoxLayout, QProgressBar, QLabel, QDesktopWidget


class Splash(QSplashScreen):
    def __init__(self):
        QSplashScreen.__init__(self)
        self.width, self.height = 400, 300  # Change to desired size
        self.setFixedSize(self.width, self.height)
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        pixmap = QPixmap("")  # Specify image path
        self.setPixmap(pixmap.scaled(400, 300))  # Rescales pixmap, match to window width and height
        self.setup()
        self.time_start = time.clock()

    def loading_update(self, percent, message):
        """
        Call this method from the main_window class or other active class to tell the splash screen to update
        the prgoress bar and loading message.
        percent: int or float
        message: str
        """
        
        self.message_display.setText(message)
        if percent == 100:
            seconds = time.clock()
            while seconds < 2.5:
                time.sleep(0.5)
                seconds = time.clock()
                status = round(seconds * 40, 0)
                self.bar.setValue(status)
            self.hide()
        else:
            seconds = time.clock()
            status = min(percent, round(seconds * 20, 0))
            self.bar.setValue(status)

    def setup(self):
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
        self.message_display = QLabel(text="Loading...")  # Change message as desired
        self.layout.addWidget(self.message_display)

        self.centre_on_screen()

    def centre_on_screen(self):
        centre = QDesktopWidget().availableGeometry().center()
        x, y = centre.x() - self.width / 2, centre.y() - self.height / 2
        x = 0 if x < 0 else x
        y = 0 if y < 0 else y
        self.move(x, y)
