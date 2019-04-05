# Basic skeleton for a working program

Includes a main window template, a main window class, and a run function. The template looks after the background construction of the main window's menu bar, and what happens when a menu item is selected. It includes specification of window name, centres the window on open, and sets the starting window size. Main window class sets up a stacked widget to which individual pages can be addded from import page classes.

Customize the self.menu function in main window class to specify menu items. Customize self.page_names and self.setup_pages function to add page class instances.

run.py runs the program
