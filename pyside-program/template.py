from PySide2.QtCore import QMetaObject, QCoreApplication
from PySide2.QtWidgets import QWidget, QMainWindow, QDesktopWidget, QStackedWidget, QMenuBar, QMenu, QAction, QStatusBar


class MainWindowTemplate(QMainWindow):
    """
    Template for main window that sets window size and placement, creates menu and status bars, and handles menu
    signals.
    """

    def __init__(self, title=""):
        QMainWindow.__init__(self)
        self.setObjectName("MainGUI")
        self.screen = QDesktopWidget().availableGeometry()
        self.setup_template(title)

    def menu_signals(self):
        """Interprets the selection of a menu item or subitem and sends the appropriate signal via menu_connections"""
        
        for head, option in self.menu_items.items():
            for item, widget in option.items():
                if type(widget) == list:  # Open a side menu for any menu item with a list of subitems
                    for subitem, subwidget in widget[1].items():
                        subwidget.triggered.connect(self.menu_connections(head, item, subitem))
                else:
                    widget.triggered.connect(self.menu_connections(head, item))

    def menu_connections(self, head, item, subitem=None):
        """Redirects menu signals to the menu_operations function in the main window class"""
        return lambda: self.menu_operations(head, item, subitem)

    def setup_template(self, title):
        self.resize(self.screen.width() - 150, self.screen.height() - 150)  # Sets window size 150 px from screen edge
        self.centre_on_screen()
        QMetaObject.connectSlotsByName(self)
        _translate = QCoreApplication.translate
        self.setWindowTitle(title)

    def centre_on_screen(self):
        centre = self.screen.center()
        x, y = centre.x() - self.size().width() / 2, centre.y() - self.size().height() / 2
        x = 0 if x < 0 else x
        y = 0 if y < 0 else y
        self.move(x, y)

    def setup_menu(self):
        """Builds a dictionary of menu item instances based on the menu items specified in main window class"""
        
        self.menu_bar = QMenuBar(self)
        self.menu_heads = {}
        self.menu_items = {}

        for head, items in self.menu_list.items():
            self.menu_heads[head] = QMenu(self.menu_bar)
            self.menu_bar.addAction(self.menu_heads[head].menuAction())
            self.menu_items[head] = {}
            for item in items:
                if type(item) == str:
                    if item == "-----":
                        self.menu_heads[head].addSeparator()
                    else:
                        self.menu_items[head][item] = QAction(self)
                        self.menu_heads[head].addAction(self.menu_items[head][item])
                elif type(item) == list:
                    root = item[0]
                    self.menu_items[head][root] = []
                    self.menu_items[head][root].append(QMenu(self.menu_heads[head]))
                    self.menu_heads[head].addAction(self.menu_items[head][root][0].menuAction())
                    self.menu_items[head][root].append({})
                    for subitem in item[1]:
                        self.menu_items[head][root][1][subitem] = QAction(self)
                        self.menu_items[head][root][0].addAction(self.menu_items[head][root][1][subitem])

        self.setMenuBar(self.menu_bar)

        _translate = QCoreApplication.translate
        for menu_head, widget in self.menu_heads.items():
            widget.setTitle(_translate("MainGUI", menu_head))
        for menu_head, menu_item in self.menu_items.items():
            for item, widget in menu_item.items():
                if type(widget) == list:
                    widget[0].setTitle(_translate("MainGUI", item))
                    for subitem, subwidget in widget[1].items():
                        subwidget.setText(_translate("MainGUI", subitem))
                else:
                    if item != '-----':
                        widget.setText(_translate("MainGUI", item))

    def setup_status(self):
        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)
