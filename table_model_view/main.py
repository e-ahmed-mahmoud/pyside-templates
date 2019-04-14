#!/usr/bin/env python3
#
#   main.py
#   Implements examples of table model, table proxy model, and table view classes in a simple frame.
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


from PySide2.QtWidgets import QFrame, QVBoxLayout, QTableView
from table_models import TableModel


class MainFrame(QFrame):
    def __init__(self):
        """
        Basic widget to display an example of a table view with underlying model and proxy model
        Either read or directly define: a list of column names, a list of lists (row[column]) holding table data, and
        a dict of dicts holding information (Type, Label, Alignment, Width, and other other info) for each column name.
        """

        super().__init__()
        columns = ["name", "number1", "number2"]
        data = [["David", 4, 6], ["David", 5, 2], ["Sarah", 0, 2], ["Evan", 9, 1], ["Leah", 6, 4]]
        info = {"name": {"Type": "str", "Label": "Name", "Alignment": "left", "Width": 120},
                "number1": {"Type": "int", "Label": "Number 1", "Alignment": "center", "Width": 80},
                "number2": {"Type": "int", "Label": "Number 2", "Alignment": "center", "Width": 80}}
        self.table_model = TableModel(columns, data, info)
        self.table_view = QTableView()
        self.table_view.setModel(self.table_model)
        self.setup()

    def setup(self):
        layout = QVBoxLayout(self)
        layout.addWidget(self.table_view)
