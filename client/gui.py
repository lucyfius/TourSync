import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from api_client import TourAPIClient
from config import validate_config
import tkcalendar

class TourSchedulerApp:
    def __init__(self, root):
        validate_config()
        
        self.root = root
        self.root.title("Property Tour Scheduler")
        self.api_client = TourAPIClient()
        
        # Create main frames
        self.create_widgets()
        self.refresh_tours()

    def create_widgets(self):
        # Create frames
        self.left_frame = ttk.Frame(self.root, padding="10")
        self.left_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.right_frame = ttk.Frame(self.root, padding="10")
        self.right_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Schedule Tour Form
        ttk.Label(self.left_frame, text="Schedule New Tour", font=('Helvetica', 12, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)
        
        # Property ID
        ttk.Label(self.left_frame, text="Property ID:").grid(row=1, column=0, sticky=tk.W)
        self.property_id_var = tk.StringVar()
        ttk.Entry(self.left_frame, textvariable=self.property_id_var).grid(row=1, column=1, padx=5, pady=5)

        # Client Name
        ttk.Label(self.left_frame, text="Client Name:").grid(row=2, column=0, sticky=tk.W)
        self.client_name_var = tk.StringVar()
        ttk.Entry(self.left_frame, textvariable=self.client_name_var).grid(row=2, column=1, padx=5, pady=5)

        # Date Picker
        ttk.Label(self.left_frame, text="Date:").grid(row=3, column=0, sticky=tk.W)
        self.date_picker = tkcalendar.DateEntry(self.left_frame, width=12, background='darkblue',
                                              foreground='white', borderwidth=2)
        self.date_picker.grid(row=3, column=1, padx=5, pady=5)

        # Time Entry
        ttk.Label(self.left_frame, text="Time (HH:MM):").grid(row=4, column=0, sticky=tk.W)
        self.time_var = tk.StringVar(value="09:00")
        ttk.Entry(self.left_frame, textvariable=self.time_var).grid(row=4, column=1, padx=5, pady=5)

        # Submit Button
        ttk.Button(self.left_frame, text="Schedule Tour", command=self.schedule_tour).grid(row=5, column=0, columnspan=2, pady=20)

        # Tours List
        ttk.Label(self.right_frame, text="Scheduled Tours", font=('Helvetica', 12, 'bold')).grid(row=0, column=0, pady=10)
        
        # Create Treeview
        self.tree = ttk.Treeview(self.right_frame, columns=('Date', 'Time', 'Property', 'Client'), show='headings')
        self.tree.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Add headings
        self.tree.heading('Date', text='Date')
        self.tree.heading('Time', text='Time')
        self.tree.heading('Property', text='Property')
        self.tree.heading('Client', text='Client')

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.right_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        self.tree.configure(yscrollcommand=scrollbar.set)

    def refresh_tours(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Fetch and display tours
        tours = self.api_client.get_tours()
        for tour in tours:
            tour_time = datetime.fromisoformat(tour['tour_time'])
            self.tree.insert('', 'end', values=(
                tour_time.strftime('%Y-%m-%d'),
                tour_time.strftime('%H:%M'),
                tour['property_id'],
                tour['client_name']
            ))

    def schedule_tour(self):
        try:
            # Get date and time
            date = self.date_picker.get_date()
            time_str = self.time_var.get()
            hour, minute = map(int, time_str.split(':'))
            
            # Combine date and time
            tour_time = datetime.combine(date, datetime.min.time().replace(hour=hour, minute=minute))
            
            # Create tour
            result = self.api_client.create_tour(
                property_id=self.property_id_var.get(),
                tour_time=tour_time,
                client_name=self.client_name_var.get()
            )

            if result:
                messagebox.showinfo("Success", "Tour scheduled successfully!")
                self.refresh_tours()
                # Clear form
                self.property_id_var.set("")
                self.client_name_var.set("")
                self.time_var.set("09:00")
            else:
                messagebox.showerror("Error", "Failed to schedule tour")
                
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TourSchedulerApp(root)
    root.mainloop()
