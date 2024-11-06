import tkinter as tk
from gui import TourSchedulerApp

def main():
    root = tk.Tk()
    
    # Set window size and position
    window_width = 1200
    window_height = 700
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - window_width/2)
    center_y = int(screen_height/2 - window_height/2)
    
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    root.minsize(1000, 600)
    
    # Configure main window
    root.configure(bg='#F8FAFC')
    root.title("TourSync")
    
    # Create the app
    app = TourSchedulerApp(root)
    
    root.mainloop()

if __name__ == "__main__":
    main()
