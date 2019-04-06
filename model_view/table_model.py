"""
This module contains classes for creating and interacting with a model-view table system, including an abstract table model, sort proxy filter model, and one or more table views. It allows table data, objects, and operations to be housed within a single class. Data currently need to be in the form of a list of column names, a list of lists containing row data, and a list of dictionaries containing details about the table columns (e.g. specified column width).

To do: Add option to format data and columns from a pandas dataframe; Add context menu building; Add editability; Add customizeable filters
"""


from PySide2.QtWidgets import QTableView, QAbstractItemView, QSizePolicy, QMenu
from PySide2.QtCore import QAbstractTableModel, Qt, QSortFilterProxyModel


class Table:
    def __init__(self, name, parent=None, columns=[], data=[[]], info=None):
        self.name = name
        self.parent = parent
        columns_to_model = columns
        data_to_model = dataset
        self.model = TableModel(columns_to_model, data_to_model, info)
        self.proxy_model = ProxyModel(self.model)
        self.tables = {}

    def add_table(self, name):
        self.tables[name] = TableView(self, name, self.proxy_model)

    def table_view(self, name):
        return self.tables[name]

    def add_record(self, record):
        self.model.dataset.append(record)
        self.refresh()

    def delete_record(self, i):
        self.model.dataset.pop(i)
        self.refresh()

    def refresh(self):
        self.model.beginResetModel()
        self.model.endResetModel()


class TableModel(QAbstractTableModel):
    def __init__(self, columns, dataset, info):
        super().__init__()
        self.columns = columns
        self.dataset = dataset
        self.info = info

    def data(self, index, role):
        row = index.row()
        column = index.column()

        if role in [Qt.DisplayRole, Qt.EditRole]:
            column_name = self.columns[column]
            if self.info[column_name]["Type"] == "int":
                return int(self.dataset[row][column])
            elif self.info[column_name]["Type"] == "float":
                return float(self.dataset[row][column])
            return str(self.dataset[row][column])
        return None

    def setData(self, index, value, role):
        if role == Qt.EditRole:
            row = index.row()
            column = index.column()
            self.dataset[row][column] = value
            return True
        return False

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                column_name = self.columns[section]
                return self.info[column_name]["Label"]
        return None

    def rowCount(self, parent=None):
        return len(self.dataset)

    def columnCount(self, parent=None):
        return len(self.columns)

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable


class ProxyModel(QSortFilterProxyModel):
    def __init__(self, model):
        super().__init__()
        self.setSourceModel(model)
        self.filter_conditions = {"Remove": []}

    def filterAcceptsRow(self, source_row, source_parent):
        if source_row in self.filter_conditions["Remove"]:
            return False
        
        # Add any necessary filtering operations here. You can add items to self.filter_conditions before filtering
        # and then call upon that to control filtering here. Return False for every row to be excluded, the True at
        # the end of the method will return all remaining rows.
        
        return True
