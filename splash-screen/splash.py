import time
from PySide2.QtCore import Qt
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QSplashScreen, QVBoxLayout, QProgressBar, QLabel, QDesktopWidget


class Splash(QSplashScreen):
    def __init__(self, image, width=400, height=300):
        """
        :image: str, file path to background image
        :width: int, specified width for splash screen
        :height: in, specified height for splash screen
        """
        super().__init__(self)
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
        centre = QDesktopWidget().availableGeometry().center()
        x, y = centre.x() - self.width / 2, centre.y() - self.height / 2
        x = 0 if x < 0 else x
        y = 0 if y < 0 else y
        self.move(x, y)
