# Template for creating a main window

This creates a functioning main window with a customized menu bar, status bar, window title, and icon. Use run.py to run the program.

If using MainWindow class as a template, subclass it and reimplement the menu() and menu_operations() methods, and direct run.py to import and call the subclass. Either the subclass or the instance should specify "title" (str name for window), "icon" (str file path to image), and "object_name" (str defaults to "MainWindow") if desired.

The window is set to scale to desktop screen size with 150 pixels space on each side. The window will centre on screen when opened.
