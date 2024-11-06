import tkinter as tk
from gui import TourSchedulerApp
from config import validate_config

def main():
    # Initialize the main window
    root = tk.Tk()
    
    # Set window size
    root.geometry("800x600")
    
    # Create the app
    app = TourSchedulerApp(root)
    
    # Start the main event loop
    root.mainloop()

if __name__ == "__main__":
    main()
