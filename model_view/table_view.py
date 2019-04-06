from PySide2.QtWidgets import QTableView


class TableView(QTableView):
    def __init__(self, parent, name, model, columns_to_include=[], rotated=False, stretch=False):
        super().__init__()
        self.parent = parent
        self.name = name
        self.model = model
        self.setup(rotated, stretch)
        self.setModel(self.model)
        self.setSortingEnabled(True)
        if columns_to_include:  # List of column names if not all columns are to be visible
            self.set_columns(columns_to_include)
        self.set_widths()
        self.fit_rows()

    def set_columns(self, columns_to_include):
        if columns_to_include:
            for i, column in enumerate(self.model.sourceModel().columns):
                if column not in columns_to_include:
                    self.setColumnHidden(i, True)
                    
    def show_all_columns(self):
        """Call this before calling set_columns to change the visible columns"""
        for i in range(len(self.model.sourceModel().columns)):
            self.setColumnHidden(i, False)
    
    def set_widths(self):
        for i, column in enumerate(self.model.sourceModel().columns):
            width = self.model.sourceModel().info[column]["Width"]
            self.setColumnWidth(i, width)

    def fit_rows(self):
        for row in range(self.model.rowCount()):
            self.resizeRowToContents(row)
    
    def setup(self, rotated, stretch):
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        if rotated:
            self.setHorizontalHeader(RotatedHeader(self))
        self.horizontalHeader().setStretchLastSection(stretch)
        self.setAlternatingRowColors(True)
        self.setShowGrid(False)

    def contextMenuEvent(self, event):
        index = self.indexAt(event.pos())
        row = self.model.mapToSource(index).row()
        column = self.model.mapToSource(index).column()
        column_name = self.model.sourceModel().columns[column]
        context_menu = QMenu(self)
        menu_items = {}

        
class RotatedHeader(QHeaderView):
    """Instantiate this class in table view with: self.setHorizontalHeader(RotatedHeader(self))"""
    def __init__(self, parent):
        super().__init__(Qt.Horizontal, parent=parent)
        self.setSectionsClickable(True)

    def paintSection(self, painter, rect, index):
        painter.save()
        painter.translate(rect.x(), rect.y() + rect.height())
        painter.rotate(-90)
        new_rect = QRect(0, 0, rect.height(), rect.width())
        super(RotatedHeader, self).paintSection(painter, new_rect, index)
        painter.restore()
        
        # There should be a way to simplify this to using whatever os style
        if 'win' in sys.platform:
            if index > 0:
                painter.setPen(QColor(230, 230, 230))
                painter.drawLine(rect.x() + rect.width() - 1, rect.y(),
                                 rect.x() + rect.width() - 1, rect.y() + rect.height())

    def minimumSizeHint(self):
        size = super(RotatedHeader, self).minimumSizeHint()
        size.transpose()

        return size

    def sectionSizeFromContents(self, index):
        size = super(RotatedHeader, self).sectionSizeFromContents(index)
        size.transpose()

        return size
