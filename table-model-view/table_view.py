#!/usr/bin/env python3
#
#   table_view.py
#   Example of table view subclass for use with a ProxyModel
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


import io
import csv
from PySide2.QtWidgets import QTableView, QAbstractItemView, QSizePolicy, QMenu, qApp


class TableView(QTableView):
    def __init__(self, parent, model, name):
        """
        Subclass of QTableView. Allows setting custom column widths and a context (right click) menu to remove
        rows from the view (without deleting them from the data). Set some basic customization options which can be
        changed as desired.

        :param parent: parent widget which holds the table view
        :param model: QSortFilterProxyModel object
        :param name: str, name of the table
        """

        super().__init__()
        self.parent = parent
        self.model = model
        self.name = name
        self.setup()
        self.setModel(model)
        self.setSortingEnabled(True)
        self.set_widths()
        self.fit_rows()

    def setup(self):
        """Sets some basic customization options"""

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.horizontalHeader().setStretchLastSection(False)
        self.setAlternatingRowColors(True)
        self.setShowGrid(False)

    def set_widths(self):
        """Reads information from the info dictionary in the underlying source model (TableModel) and sets the
        specified widths for each column"""

        columns = self.model.sourceModel().columns
        for i, column in enumerate(columns):
            width = self.model.sourceModel().info[column]["Width"]
            self.setColumnWidth(i, width)

    def set_visible_columns(self, columns_to_include=[]):
        """
        Hides columns so that only those specified in the columns_to_include list are shown
        
        :param columns_to_include: list of str, items must be column names as defined in the underlying TableModel
        """
        
        for i, column in enumerate(self.model.sourceModel().columns):
            hide = column not in columns_to_include
            self.setColumnHidden(i, hide)
    
    def fit_rows(self):
        """Adjusts row heights to fit all data"""

        for row in range(self.model.sourceModel().rowCount()):
            self.resizeRowToContents(row)

    def contextMenuEvent(self, event):
        """
        Sets up the menu to show when a cell is right-clicked. This example includes a 'Remove' option which, when
        selected, adds the clicked row to a list of rows to be filtered out and calls the filtering method for the
        proxy model to hide the row. Different context menus can be set up for different columns if desired by reading
        the column number from the index, cross-checking it with the columns list in the source model, and building
        the menu items under if else statements (e.g. if column_name == "Column A").

        :param event: right click event, used to access the index (row/column) which was clicked
        """

        index = self.indexAt(event.pos())
        row = self.model.mapToSource(index).row()
        context_menu = QMenu(self)
        menu_items = {}
        for item in ["Copy", "Remove"]:  # Build menu first
            menu_items[item] = context_menu.addAction(item)
        selection = context_menu.exec_(event.globalPos())  # Identify the selected item
        if selection == menu_items["Copy"]:  # Specify what happens for each item
            self.copy_selection()
        elif selection == menu_items["Remove"]:
            self.model.filter_conditions["Remove"].append(row)
            self.model.setFilterFixedString("")

    def copy_selection(self):
        """
        This function copies the selected cells in a table view, accounting for filters and rows as well as
        non-continuous selection ranges. The format of copied values can be pasted into Excel retaining the
        original organization.
        
        Adapted from code provided by ekhumoro on StackOverflow 
        """
        
        selection = self.selectedIndexes()
        if selection:
            rows = [index.row() for index in selection]
            columns = [index.column() for index in selection]
            row_count = max(rows) - min(rows) + 1
            col_count = max(columns) - min(columns) + 1
            table = [[""] * col_count for _ in range(row_count)]
            for index in selection:
                row = index.row() - min(rows)
                column = index.column() - min(columns)
                table[row][column] = index.data()
            stream = io.StringIO()
            csv.writer(stream, delimiter="\t").writerows(table)
            qApp.clipboard().setText(stream.getvalue())
