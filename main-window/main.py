#!/usr/bin/env python3
#
#   main.py
#   A main window template including customized menu bar.
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


from PySide2.QtWidgets import QMainWindow, QDesktopWidget, QMenuBar, QMenu, QAction, QStatusBar
from PySide2.QtCore import QCoreApplication
from PySide2.QtGui import QIcon


class MainWindow(QMainWindow):
    def __init__(self, title="", icon="", object_name="MainWindow"):
        """
        Template for main window that sets window size and placement, creates menu and status bars, and handles menu
        signals.
    
        :param title: str; Name to be displayed at the top of the window
        :param icon: str; file path to icon image file
        :param object_name: str; Name of main window object
        """

        super().__init__()
        self.setObjectName(object_name)
        self.screen = QDesktopWidget().availableGeometry()
        self.setup_template(title)
        if icon:
            self.setWindowIcon(QIcon(icon))
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
        Re-implement this function to define what happens when each menu item is selected.
        
        :param head: str, menu head name as defined in self.menu()
        :param item: str, menu item name as defined in self.menu()
        :param head: str, menu subitem name, if applicable, as defined in self.menu()
        """

        if head == "File":
            if item == "Close":
                self.close()

    def setup_template(self, title):
        """Sets up window size and title"""
        
        self.resize(self.screen.width() - 150, self.screen.height() - 150)  # Sets window size 150 px from screen edge
        self.centre_on_screen()
        self.setWindowTitle(title)

    def centre_on_screen(self):
        """Centers the screen on the desktop"""
        
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
        """Redirects menu signals to the menu_operations function in the main window class. Leave this."""
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
