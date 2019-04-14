# Example of table model and view implementation

Contains subclasses to implement QAbstractTableModel, QSortFilterProxyModel, and QTableView and apply delegates to replace data.

Run program from run.py

main.py contains a QFrame object which produces the TableModel, ProxyModel, and TableView instances and displays the TableView.

The example table here has a name column, two integer score columns, and a bool column indicating whether the combined score for each name is the highest total in the table. A delegate is used to fill in the high score cell with a solid color if the cell's value is True.
