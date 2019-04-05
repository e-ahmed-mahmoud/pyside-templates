from PySide2.QtWidgets import QStackedWidget
from template import MainWindowTemplate


class MainGUI(MainWindowTemplate):
    def __init__(self):
        super().__init__("Main window name")  # Enter name to be displayed at top of window
        self.menu()
        self.setup_menu()
        self.menu_signals()
        self.setup_status()
        self.central_widget = QStackedWidget()  # Provides a widget to add pages to
        self.setCentralWidget(self.central_widget)
        self.page_names = []  # Add the names of pages to be added to the stacked widget
        self.pages = self.setup_pages()
        for page in self.page_names:
            self.central_widget.addWidget(self.pages[page])
        self.central_widget.setCurrentIndex(0)

    def setup_pages(self):
        """
        The structure of this program is a set of individual pages added to a stacked widget which can be switched
        between as needed. Page classes need to be imported from their source module(s). self.page_names can be referenced
        to determine the place of each page in the stacked widget.
        """
        
        pages = {}
        page_classes = {}  # For each page name key in self.page_names, specify the page class
        for page_name in self.page_names:
            pages[page_name] = page_classes[page_name](self, page_name)  # Customize parameter inputs as needed
        return pages

    def menu_operations(self, head, item, subitem=None):
        """Defines what happens when each menu item is selected"""

        if head == "File":
            if item == "Close":
                self.close()
                
    def menu(self):
        """
        Lists all of the menu operations available in formats:
        {"Menu head": ["Menu item"]}
        {"Menu head 1": ["Menu item under 1"], "Menu head 2": ["Menu item under 2"]}
        {"Menu head": ["Menu item 1", "Menu item 2"]}
        {"Menu head": [{"Menu item 1: ["Menu subitem 1", "Menu subitem 2"]}, "Menu item 2"]}
        For a line between menu items, specify five dashes, e.g. {"Menu head": ["Menu item 1", "-----", "Menu item 2"]}
        """

        self.menu_list = {"File": ["Close"]}
        
