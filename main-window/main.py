#!/usr/bin/env python3
# Libraries needed: PySide2


from PySide2.QtWidgets import QMainWindow, QDesktopWidget, QMenuBar, QMenu, QAction, QStatusBar
from PySide2.QtCore import QMetaObject, QCoreApplication
from PySide2.QtGui import QIcon


class MainWindow(QMainWindow):
    """
    Template for main window that sets window size and placement, creates menu and status bars, and handles menu
    signals.
    """

    def __init__(self, title="", icon="", object_name="MainWindow"):
        """
        :title: str; Name to be displayed at the top of the window
        :icon: str; file path to icon image file
        :object_name: str; Name of main window object
        """

        super().__init__()
        self.setObjectName(object_name)
        self.screen = QDesktopWidget().availableGeometry()
        self.setup_template(title)
        if icon:
            self.setWindowIcon(QIcon(""))
        self.menu_list = self.menu()
        self.menu_bar = QMenuBar(self)
        self.menu_heads = {}
        self.menu_items = {}
        self.setup_menu(object_name)
        self.menu_signals()
        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)

    def menu(self):
        """
        Re-implement this function to define the window menu

        Lists all of the menu operations available in formats:
        {"Menu head": ["Menu item"]}
        {"Menu head 1": ["Menu item under 1"], "Menu head 2": ["Menu item under 2"]}
        {"Menu head": ["Menu item 1", "Menu item 2"]}
        {"Menu head": [["Menu item 1, ["Menu subitem 1", "Menu subitem 2"]], "Menu item 2"]}
        Notice that if subitems are desired, the format is to replace "Menu item" with ["Menu item", [subitems]]
        For a line between menu items, specify five dashes, e.g. {"Menu head": ["Menu item 1", "-----", "Menu item 2"]}
        """

        menu = {"File": ["Close"],
                "Example": ["Item",
                            ["Item with subitems", ["Subitem 1", "Subitem 2"]],
                            "-----",
                            "Another item"
                            ]}
        return menu

    def menu_operations(self, head, item, subitem=None):
        """
        Re-implement this function to define menu operations

        Defines what happens when each menu item is selected
        """

        if head == "File":
            if item == "Close":
                self.close()

    def setup_template(self, title):
        self.resize(self.screen.width() - 150, self.screen.height() - 150)  # Sets window size 150 px from screen edge
        self.centre_on_screen()
        self.setWindowTitle(title)

    def centre_on_screen(self):
        centre = self.screen.center()
        x, y = centre.x() - self.size().width() / 2, centre.y() - self.size().height() / 2
        x = 0 if x < 0 else x
        y = 0 if y < 0 else y
        self.move(x, y)

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

    def setup_menu(self, object_name):
        """Builds a dictionary of menu item instances based on the menu items specified in menu method"""

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
            widget.setTitle(_translate(object_name, menu_head))
        for menu_head, menu_item in self.menu_items.items():
            for item, widget in menu_item.items():
                if type(widget) == list:
                    widget[0].setTitle(_translate(object_name, item))
                    for subitem, subwidget in widget[1].items():
                        subwidget.setText(_translate(object_name, subitem))
                else:
                    if item != '-----':
                        widget.setText(_translate(object_name, item))
