# Spash screen to show while loading program

Splash screen class should be instantiated at the start of the main_window's __init__ method, followed by calling show(). The loading_update() method should be called as necessary to update the progress bar (int of percentage loaded) and loading message (str). Loading update must be called with 100 as percent parameter in order to close splash screen.

User must specify the image path for background image of splash screen and change the window size and image size as needed. The placement of the progress bar and message can be changed inside the setup() method.
