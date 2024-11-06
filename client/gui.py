import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from api_client import TourAPIClient
from config import validate_config
import tkcalendar
from tkinter import font

class TourSchedulerApp:
    def __init__(self, root):
        validate_config()
        
        self.root = root
        self.root.title("Property Tour Scheduler")
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure('Title.TLabel', font=('Helvetica', 16, 'bold'))
        self.style.configure('Subtitle.TLabel', font=('Helvetica', 12))
        self.style.configure('Success.TButton', background='#4CAF50')
        
        # Set background color
        self.root.configure(bg='#f0f0f0')
        
        self.api_client = TourAPIClient()
        self.create_widgets()
        self.refresh_tours()

    def create_widgets(self):
        # Main container with padding
        main_container = ttk.Frame(self.root, padding="20")
        main_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Left Frame (Schedule Form)
        self.left_frame = ttk.LabelFrame(main_container, text="Schedule New Tour", padding="15")
        self.left_frame.grid(row=0, column=0, padx=(0, 20), sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Help text
        help_text = "Fill out the form below to schedule a new property tour"
        ttk.Label(self.left_frame, text=help_text, style='Subtitle.TLabel', wraplength=250).grid(
            row=0, column=0, columnspan=2, pady=(0, 15))

        # Client Information Section
        client_frame = ttk.LabelFrame(self.left_frame, text="Client Information", padding="10")
        client_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))

        # First Name
        ttk.Label(client_frame, text="First Name:*").grid(row=0, column=0, sticky=tk.W)
        self.first_name_var = tk.StringVar()
        first_name_entry = ttk.Entry(client_frame, textvariable=self.first_name_var)
        first_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        # Last Name
        ttk.Label(client_frame, text="Last Name:*").grid(row=1, column=0, sticky=tk.W)
        self.last_name_var = tk.StringVar()
        last_name_entry = ttk.Entry(client_frame, textvariable=self.last_name_var)
        last_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        # Phone Number
        ttk.Label(client_frame, text="Phone:*").grid(row=2, column=0, sticky=tk.W)
        self.phone_var = tk.StringVar()
        phone_entry = ttk.Entry(client_frame, textvariable=self.phone_var)
        phone_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        self.create_tooltip(phone_entry, "Enter phone number (e.g., 555-555-5555)")

        # Tour Information Section
        tour_frame = ttk.LabelFrame(self.left_frame, text="Tour Details", padding="10")
        tour_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))

        # Property ID
        ttk.Label(tour_frame, text="Property ID:*").grid(row=0, column=0, sticky=tk.W)
        self.property_id_var = tk.StringVar()
        property_entry = ttk.Entry(tour_frame, textvariable=self.property_id_var)
        property_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        self.create_tooltip(property_entry, "Enter the property number here")

        # Date Picker
        ttk.Label(tour_frame, text="Tour Date:*").grid(row=1, column=0, sticky=tk.W)
        self.date_picker = tkcalendar.DateEntry(
            tour_frame,
            width=20,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            date_pattern='yyyy-mm-dd'
        )
        self.date_picker.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        # Time Selection
        ttk.Label(tour_frame, text="Tour Time:*").grid(row=2, column=0, sticky=tk.W)
        self.time_var = tk.StringVar(value="09:00 AM")
        times = [f"{h:02d}:00 {ap}" for h in range(9, 18) for ap in ('AM', 'PM')]  # 9 AM to 5 PM
        self.time_combo = ttk.Combobox(tour_frame, textvariable=self.time_var, values=times, state='readonly')
        self.time_combo.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

        # Required fields note
        ttk.Label(self.left_frame, text="* Required fields", 
                 font=('Helvetica', 8, 'italic')).grid(row=3, column=0, columnspan=2, pady=(0, 10), sticky=tk.W)

        # Submit Button
        submit_btn = ttk.Button(
            self.left_frame,
            text="Schedule Tour",
            command=self.schedule_tour,
            style='Success.TButton'
        )
        submit_btn.grid(row=4, column=0, columnspan=2, pady=10, sticky=tk.EW)

        # Right Frame (Tours List) - Update columns
        self.right_frame = ttk.LabelFrame(main_container, text="Scheduled Tours", padding="15")
        self.right_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Create Treeview with updated columns
        self.tree = ttk.Treeview(
            self.right_frame,
            columns=('Date', 'Time', 'Name', 'Phone', 'Property'),
            show='headings',
            height=15
        )
        
        # Configure columns with sorting
        column_widths = {
            'Date': 100,
            'Time': 80,
            'Name': 150,
            'Phone': 120,
            'Property': 100
        }
        
        for col, width in column_widths.items():
            self.tree.heading(col, text=col, 
                             command=lambda c=col: self.sort_treeview(c))
            self.tree.column(col, width=width)

        self.tree.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Scrollbar
        scrollbar = ttk.Scrollbar(self.right_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Refresh button
        ttk.Button(
            self.right_frame,
            text="↻ Refresh List",
            command=self.refresh_tours
        ).grid(row=2, column=0, pady=(10, 0), sticky=tk.E)

    def create_tooltip(self, widget, text):
        def show_tooltip(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            label = ttk.Label(tooltip, text=text, background="#ffffe0", relief='solid', borderwidth=1)
            label.pack()
            
            def hide_tooltip():
                tooltip.destroy()
            
            widget.tooltip = tooltip
            widget.bind('<Leave>', lambda e: hide_tooltip())
            
        widget.bind('<Enter>', show_tooltip)

    def schedule_tour(self):
        if not self.validate_inputs():
            return
            
        try:
            # Parse time
            time_str = self.time_var.get()
            time_format = "%I:%M %p"
            parsed_time = datetime.strptime(time_str, time_format)
            
            # Combine date and time
            date = self.date_picker.get_date()
            tour_time = datetime.combine(date, parsed_time.time())
            
            # Format client name
            client_name = f"{self.first_name_var.get().strip()} {self.last_name_var.get().strip()}"
            
            result = self.api_client.create_tour(
                property_id=self.property_id_var.get().strip(),
                tour_time=tour_time,
                client_name=client_name,
                phone_number=self.phone_var.get().strip()
            )

            if result:
                messagebox.showinfo("Success", "Tour scheduled successfully! ✓")
                self.refresh_tours()
                self.clear_form()
            else:
                messagebox.showerror("Error", "Unable to schedule tour. Please try again.")
                
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def validate_inputs(self):
        validation_fields = [
            (self.first_name_var.get().strip(), "First Name"),
            (self.last_name_var.get().strip(), "Last Name"),
            (self.phone_var.get().strip(), "Phone Number"),
            (self.property_id_var.get().strip(), "Property ID")
        ]
        
        for value, field_name in validation_fields:
            if not value:
                messagebox.showwarning("Missing Information", f"Please enter {field_name}")
                return False

        # Validate phone number format
        phone = self.phone_var.get().strip()
        cleaned_phone = ''.join(filter(str.isdigit, phone))
        if len(cleaned_phone) != 10:
            messagebox.showwarning("Invalid Input", 
                "Please enter a valid 10-digit phone number\nExample: 555-555-5555")
            return False
            
        return True

    def clear_form(self):
        self.first_name_var.set("")
        self.last_name_var.set("")
        self.phone_var.set("")
        self.property_id_var.set("")
        self.time_var.set("09:00 AM")
        self.date_picker.set_date(datetime.now())

    def refresh_tours(self):
        """Refresh the tours list"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            # Fetch tours
            tours = self.api_client.get_tours()
            
            # Convert to list and sort by tour time
            sorted_tours = sorted(
                tours,
                key=lambda x: datetime.fromisoformat(x['tour_time'])
            )
            
            # Display tours
            for tour in sorted_tours:
                # Parse the ISO format datetime
                tour_time = datetime.fromisoformat(tour['tour_time'])
                
                # Format date and time for display
                date_str = tour_time.strftime('%Y-%m-%d')
                time_str = tour_time.strftime('%I:%M %p')
                
                # Insert into tree view
                self.tree.insert('', 'end', values=(
                    date_str,
                    time_str,
                    tour['client_name'],
                    tour.get('phone_number', 'N/A'),
                    tour['property_id']
                ))
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh tours: {str(e)}")

    def sort_treeview(self, col):
        """Sort treeview content when header is clicked"""
        # Get all items
        items = [(self.tree.set(item, col), item) for item in self.tree.get_children('')]
        
        # Sort items
        items.sort(reverse=hasattr(self, '_sort_reverse') and self._sort_reverse)
        
        # Toggle sort direction for next click
        self._sort_reverse = not getattr(self, '_sort_reverse', False)
        
        # Rearrange items in sorted positions
        for index, (_, item) in enumerate(items):
            self.tree.move(item, '', index)
        
        # Update header to indicate sort direction
        self.tree.heading(col, text=f"{col} {'↑' if self._sort_reverse else '↓'}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TourSchedulerApp(root)
    root.mainloop()
