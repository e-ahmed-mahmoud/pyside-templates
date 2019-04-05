import sys
from PySide2.QtWidgets import QApplication
from main import MainGUI


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainGUI()  # Main window class
    ex.show()
    sys.exit(app.exec_())
