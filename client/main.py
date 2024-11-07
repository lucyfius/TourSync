import tkinter as tk
from gui import ModernUI

def main():
    root = tk.Tk()
    root.title("TourSync")
    root.geometry("1200x800")
    
    # Configure grid weight
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    
    # Create and pack the modern UI
    app = ModernUI(root)
    app.pack(fill='both', expand=True)
    
    root.mainloop()

if __name__ == "__main__":
    main()
