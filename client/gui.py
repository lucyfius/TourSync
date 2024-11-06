import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import requests
import json
from config import API_BASE_URL, validate_config

class TourSchedulerApp:
    def __init__(self, root):
        # Validate configuration before starting
        validate_config()
        
        self.root = root
        self.root.title("Property Tour Scheduler")
        self.api_base_url = API_BASE_URL
        
        # Create main frames
        self.create_widgets()
        self.refresh_tours()

    def create_widgets(self):
        # Schedule viewer
        schedule_frame = ttk.LabelFrame(self.root, text="Current Schedule")
        schedule_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
        
        self.tree = ttk.Treeview(schedule_frame, columns=("Time", "Property", "Client", "Status"))
        self.tree.heading("Time", text="Time")
        self.tree.heading("Property", text="Property")
        self.tree.heading("Client", text="Client")
        self.tree.heading("Status", text="Status")
        self.tree.grid(row=0, column=0, padx=5, pady=5)

        # New tour form
        form_frame = ttk.LabelFrame(self.root, text="Schedule New Tour")
        form_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        
        ttk.Label(form_frame, text="Property ID:").grid(row=0, column=0, padx=5, pady=5)
        self.property_id = ttk.Entry(form_frame)
        self.property_id.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Client Name:").grid(row=1, column=0, padx=5, pady=5)
        self.client_name = ttk.Entry(form_frame)
        self.client_name.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Date (YYYY-MM-DD):").grid(row=2, column=0, padx=5, pady=5)
        self.date = ttk.Entry(form_frame)
        self.date.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Time (HH:MM):").grid(row=3, column=0, padx=5, pady=5)
        self.time = ttk.Entry(form_frame)
        self.time.grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Button(form_frame, text="Schedule Tour", command=self.schedule_tour).grid(row=4, column=0, columnspan=2, pady=10)
        
        # Refresh button
        ttk.Button(self.root, text="Refresh Schedule", command=self.refresh_tours).grid(row=2, column=0, pady=10)

    def refresh_tours(self):
        try:
            response = requests.get(f"{self.api_base_url}/tours")
            tours = response.json()
            
            # Clear existing items
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Add tours to treeview
            for tour in tours:
                tour_time = datetime.fromisoformat(tour['tour_time'])
                self.tree.insert("", "end", values=(
                    tour_time.strftime("%Y-%m-%d %H:%M"),
                    tour['property_id'],
                    tour['client_name'],
                    tour['status']
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch tours: {str(e)}")

    def schedule_tour(self):
        try:
            tour_datetime = f"{self.date.get()}T{self.time.get()}:00"
            data = {
                "property_id": self.property_id.get(),
                "client_name": self.client_name.get(),
                "tour_time": tour_datetime
            }
            
            response = requests.post(f"{self.api_base_url}/tours", json=data)
            
            if response.status_code == 201:
                messagebox.showinfo("Success", "Tour scheduled successfully!")
                self.refresh_tours()
            else:
                messagebox.showerror("Error", response.json().get('error', 'Failed to schedule tour'))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to schedule tour: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TourSchedulerApp(root)
    root.mainloop()
