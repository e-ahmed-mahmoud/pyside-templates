#!/usr/bin/env python3
# Libraries needed: PySide2


import sys
from PySide2.QtWidgets import QApplication
from main import MainWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()  # Main window class
    ex.show()
    sys.exit(app.exec_())
