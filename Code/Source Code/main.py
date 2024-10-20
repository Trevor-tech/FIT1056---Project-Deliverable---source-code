import tkinter as tk
from UI.home_page import HomePage

if __name__ == "__main__":
    root = tk.Tk()  # Create the root window for the application
    home_page = HomePage(root)  # Initialize the HomePage class with the root window
    root.mainloop()  # Start the Tkinter main loop
