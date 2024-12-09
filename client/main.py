import tkinter as tk
from .gui import ModernUI
from .database import init_mongodb
from .config import validate_config, APP_NAME
import logging
from .state_manager import StateManager

def main():
    try:
        # Validate configuration
        validate_config()
        
        # Initialize MongoDB
        init_mongodb()
        
        # Initialize state manager
        state_manager = StateManager()
        
        # Create GUI
        root = tk.Tk()
        root.title(APP_NAME)
        root.geometry("1200x800")
        
        # Configure grid weight
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        
        # Create and pack the modern UI
        app = ModernUI(root, state_manager)
        app.pack(fill='both', expand=True)
        
        root.mainloop()
        
    except Exception as e:
        logging.error(f"Application failed to start: {e}")
        raise

if __name__ == "__main__":
    main()
