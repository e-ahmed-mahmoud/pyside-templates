#!/usr/bin/env python3
#
#   table_models.py
#   Examples of table model subclasses for use in PySide2 applications
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


from PySide2.QtCore import QAbstractTableModel, Qt, QSortFilterProxyModel


class TableModel(QAbstractTableModel):
    def __init__(self, columns, dataset, info):
        """
        Subclass of the QAbstractTableModel. This class holdes the table data, list of columns, and column information,
        as well as the background methods needed to communicate display information to the table view object.
        Reimplement the data(), setData, headerData(), and flags() methods, keeping the same parameters for each, to
        customize model behaviour.

        :param columns: list of column names (str)
        :param dataset: list of lists containing table data, organized as row[column]
        :param info: dictionary containing column names matching those in columns, with keys 'Label' (str), 'Width'
        (int), 'Type' (str), 'Alignment' (str), and any other column-specific info to use in model or view methods
        """

        super().__init__()
        self.columns = columns
        self.dataset = dataset
        self.info = info

    def data(self, index, role):
        """
        Determines the data to display in each cell, and its general format. Reimplemented frrom QAbstractTableModel

        :param index: a QModelIndex object referring to an individual table cell
        :param role: a Qt role to specify what sort of information is to be returned. Roles include Qt.DisplayRole,
        Qt.EditRole, Qt.TextAlignmentRole, Qt.DecorationRole, Qt.ToolTipRole, Qt.StatusTipRole, Qt.FontRole,
        Qt.BackgroundRole
        """

        row = index.row()
        column = index.column()
        column_name = self.columns[column]

        if role in [Qt.DisplayRole, Qt.EditRole]:
            if self.info[column_name]["Type"] == "int":
                return int(self.dataset[row][column])
            elif self.info[column_name]["Type"] == "float":
                return float(self.dataset[row][column])
            return str(self.dataset[row][column])
        elif role == Qt.TextAlignmentRole:
            if self.info[column_name]["Alignment"] == "right":
                return Qt.AlignRight
            elif self.info[column_name]["Alignment"] == "center":
                return Qt.AlignCenter
            return Qt.AlignLeft
        return None

    def setData(self, index, value, role=Qt.EditRole):
        """
        Relays changes made via the table view to the underlying dataset. Reimplemented frrom QAbstractTableModel

        :param index: a QModelIndex object referring to an individual table cell
        :param value: the value to be set at the specified index
        :param role: Qt role, defaults to Qt.EditRole
        """

        if role == Qt.EditRole:
            row = index.row()
            column = index.column()
            self.dataset[row][column] = value
            return True
        return False

    def headerData(self, section, orientation, role):
        """
        Determines the data to display in each row or column header, and its general format. Reimplemented frrom
        QAbstractTableModel

        :param section: int, refers to either the row number or column number, depending on orientation
        :param orientation: either Qt.Horizontal for column header or Qt.Vertical for row header
        :param role: a Qt role to specify what sort of data is to be returned. Roles include Qt.DisplayRole,
        Qt.TextAlignmentRole, Qt.ToolTipRole, Qt.StatusTipRole, Qt.FontRole, Qt.BackgroundRole
        """

        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                column_name = self.columns[section]
                return self.info[column_name]["Label"]
            elif orientation == Qt.Vertical:
                pass  # Replace with any instructions to display a either row number or a particular column as header
        elif role == Qt.TextAlignmentRole:
            if orientation == Qt.Horizontal:
                return Qt.AlignCenter
        return None

    def rowCount(self, parent=None):
        """Returns the number of rows in the model. Leave this."""

        return len(self.dataset)

    def columnCount(self, parent=None):
        """Returns the number of columns in the model. Leave this."""

        return len(self.columns)

    def flags(self, index):
        """
        Set whether individual cells are enabled, selectable and/or editable. Reimplemented frrom QAbstractTableModel

        :param index: a QModelIndex object referring to an individual table cell
        """

        return Qt.ItemIsEnabled | Qt.ItemIsSelectable


class ProxyModel(QSortFilterProxyModel):
    def __init__(self, model):
        """
        Subclass of the QSortFilterProxyModel. This class allows the table view to interact with the model indirectly
        via a middle-mas proxy that sorts or filters the table. It reimplements the filterAcceptsRow method to allow
        flexibility on how data are filtered, including filtering base on multiple columns. Reimplement
        filterAcceptsRow() method as desired. Use self.sourceModel() to refer to the underlying table model. Use
        mapToSource(index) to convert an index in the proxy model to an index in the underlying model, allowing you to
        access the respective dataset via row and column index methods.

        :param model: TableModel object holding the underlying model
        """

        super().__init__()
        self.setSourceModel(model)
        self.filter_conditions = {"Remove": []}  # Can be changed, added to and used for filterAcceptsRow filtering

    def filterAcceptsRow(self, source_row, source_parent):
        """
        Returns True if the row matches required conditions to remain in the filtered table, False to remove the row

        :param source_row: int, the row index in the source model
        :param source_parent: parent object of source model
        """

        if source_row in self.filter_conditions["Remove"]:
            return False
        for column, conditions in self.filter_conditions.items():
            if column == "Remove":
                if source_row in conditions:
                    return False
            for i, column_name in enumerate(self.sourceModel().columns):
                if column_name == column:
                    if self.sourceModel().dataset[source_row][i] not in conditions:
                        return False
        return True

    def add_filter_condition(self, column_name, conditions):
        """
        Specifies a list of values for a specified column which are to be included in a filtered table. This replaces
        any previous filter on the same column but does not reset any other filters. Use reset_filters() to reset all
        filters. Reimplement this function if you want more complicated methods of determining filter conditions, for
        example if you want to add a value to the already-existing list of conditions for a given column rather than
        replacing the conditions list entirely, or if you want to specify to exclude specified values instead of
        including them.

        :param column_name: str, name of column, must be included in the columns list of the source model
        :param conditions: list of values to be included a filter of the specified column
        """

        self.filter_conditions[column_name] = conditions
        self.setFilterFixedString("")

    def reset_filters(self):
        """Removes all filter conditions and returns the table to its original unfiltered state"""

        self.filter_conditions = {"Remove": []}
        self.setFilterFixedString("")
