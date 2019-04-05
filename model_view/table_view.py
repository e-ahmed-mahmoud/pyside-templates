class TableView(QTableView):
    def __init__(self, parent, name, model):
        super().__init__()
        self.parent = parent
        self.name = name
        self.model = model
        self.setup()
        self.setModel(self.model)
        self.setSortingEnabled(True)
        self.set_widths()
        self.fit_rows()

    def setup(self):
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.horizontalHeader().setStretchLastSection(True)
        self.setAlternatingRowColors(True)
        self.setShowGrid(False)

    def set_widths(self):
        for i, column in enumerate(self.model.sourceModel().columns):
            width = self.model.sourceModel().info[column]["Width"]
            self.setColumnWidth(i, width)

    def fit_rows(self):
        for row in range(self.model.rowCount()):
            self.resizeRowToContents(row)

    def contextMenuEvent(self, event):
        index = self.indexAt(event.pos())
        row = self.model.mapToSource(index).row()
        column = self.model.mapToSource(index).column()
        column_name = self.model.sourceModel().columns[column]
        context_menu = QMenu(self)
        menu_items = {}
