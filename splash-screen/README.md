# Spash screen to show while loading program

Splash screen class should be instantiated at the start of the main_window's __init__ method, followed by calling {SplashInstance}.show(), and loading_update method should be called as necessary to update the progress bar and loading message. Loading update must be called with 100 as percent parameter in order to close splash screen.

User must specify the image path for background image of splash screen and change the window size and image size as needed.
