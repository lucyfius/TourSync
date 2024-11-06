import tkinter as tk
from gui import TourSchedulerApp
from config import validate_config

def main():
    root = tk.Tk()
    
    # Set window size and position it in the center
    window_width = 1000
    window_height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - window_width/2)
    center_y = int(screen_height/2 - window_height/2)
    
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    root.minsize(800, 500)  # Set minimum window size
    
    # Set window title and icon
    root.title("Property Tour Scheduler - Easy Booking")
    
    # Create the app
    app = TourSchedulerApp(root)
    
    # Start the main event loop
    root.mainloop()

if __name__ == "__main__":
    main()
