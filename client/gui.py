import tkinter as tk
from tkinter import ttk, messagebox
import tkcalendar
from datetime import datetime
from api_client import TourAPIClient
from config import validate_config
from edit_tour_dialog import EditTourDialog

class TourSchedulerApp:
    def __init__(self, root):
        validate_config()
        
        self.root = root
        self.root.title("TourSync")
        
        # Modern, minimalist color scheme
        self.colors = {
            'background': '#F8FAFC',    # Very light gray/blue
            'card': '#FFFFFF',          # White
            'primary': '#3B82F6',       # Modern blue
            'secondary': '#64748B',     # Slate gray
            'text': '#1E293B',          # Dark slate
            'text_secondary': '#64748B', # Medium slate
            'border': '#E2E8F0',        # Light gray
            'hover': '#2563EB',         # Darker blue for hover
            'row_alt': '#F1F5F9'        # Alternate row color
        }

        # Initialize API client first
        self.api_client = TourAPIClient()  # Fixed variable name
        
        # Define business hours
        self.business_hours = {
            'start': 9,     # 9 AM
            'end': 17,      # 5 PM
            'lunch_start': 12,  # 12 PM
            'lunch_end': 13     # 1 PM
        }
        
        # Setup variables and UI
        self.setup_variables()
        self.setup_ui()
        self.refresh_tours()

        # Cache commonly used styles
        self.cached_styles = {}
        self.setup_cached_styles()

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Frame styles
        self.style.configure('Main.TFrame',
                           background=self.colors['background'])
        
        self.style.configure('Card.TFrame',
                           background=self.colors['card'])
        
        # Label styles
        self.style.configure('Title.TLabel',
                           font=('Segoe UI', 16, 'bold'),
                           background=self.colors['card'],
                           foreground=self.colors['text'])
        
        self.style.configure('Field.TLabel',
                           font=('Segoe UI', 11),
                           background=self.colors['card'],
                           foreground=self.colors['text_secondary'])
        
        # Modern button style
        self.style.configure('Modern.TButton',
                           font=('Segoe UI', 11),
                           background=self.colors['primary'],
                           foreground='white',
                           padding=(20, 10),
                           borderwidth=0,
                           relief='flat')
        
        self.style.map('Modern.TButton',
                      background=[('active', self.colors['hover'])])
        
        # Secondary button style
        self.style.configure('Secondary.TButton',
                           font=('Segoe UI', 11),
                           background=self.colors['secondary'],
                           foreground='white',
                           padding=(15, 8),
                           borderwidth=0)
        
        # Entry style
        self.style.configure('Modern.TEntry',
                           fieldbackground='white',
                           bordercolor=self.colors['border'],
                           lightcolor=self.colors['border'],
                           darkcolor=self.colors['border'],
                           borderwidth=1,
                           relief='flat',
                           padding=8)
        
        # Treeview style
        self.style.configure('Modern.Treeview',
                           background='white',
                           fieldbackground='white',
                           foreground=self.colors['text'],
                           rowheight=40,
                           borderwidth=0)
        
        self.style.configure('Modern.Treeview.Heading',
                           font=('Segoe UI', 11, 'bold'),
                           background='white',
                           foreground=self.colors['text'],
                           padding=12,
                           borderwidth=0)
        
        # Remove borders
        self.style.layout('Modern.Treeview', [('Modern.Treeview.treearea', {'sticky': 'nswe'})])

    def create_layout(self):
        # Main container with padding
        main = ttk.Frame(self.root, style='Main.TFrame')
        main.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Configure grid
        main.columnconfigure(0, weight=4)  # Form section
        main.columnconfigure(1, weight=5)  # List section
        main.rowconfigure(0, weight=1)
        
        # Create sections
        self.create_form_section(main)
        self.create_list_section(main)

    def create_form_section(self, parent):
        form_card = ttk.Frame(parent, style='Card.TFrame', padding=25)
        form_card.grid(row=0, column=0, sticky='nsew', padx=(0, 20))
        
        # Add subtle shadow to card
        form_card.configure(relief='solid', borderwidth=1)
        
        ttk.Label(form_card,
                 text="Schedule New Tour",
                 style='Title.TLabel').pack(anchor='w', pady=(0, 25))
        
        # Form fields with modern styling
        fields = [
            ("First Name", self.first_name_var),
            ("Last Name", self.last_name_var),
            ("Phone Number", self.phone_var),
            ("Property ID", self.property_id_var)
        ]
        
        for label, var in fields:
            self.create_form_field(form_card, label, var)
        
        # Date and time selectors
        self.create_datetime_selectors(form_card)
        
        # Submit button with modern style
        submit_btn = ttk.Button(form_card,
                              text="Schedule Tour",
                              style='Modern.TButton',
                              command=self.schedule_tour)
        submit_btn.pack(pady=(25, 0), fill='x')

    def create_list_section(self, parent):
        list_card = ttk.Frame(parent, style='Card.TFrame', padding=25)
        list_card.grid(row=0, column=1, sticky='nsew')
        list_card.configure(relief='solid', borderwidth=1)
        
        # Header with refresh button
        header = ttk.Frame(list_card, style='Card.TFrame')
        header.pack(fill='x', pady=(0, 20))
        
        ttk.Label(header,
                 text="Upcoming Tours",
                 style='Title.TLabel').pack(side='left')
        
        ttk.Button(header,
                  text="Refresh",
                  style='Secondary.TButton',
                  command=self.refresh_tours).pack(side='right')
        
        self.create_tours_treeview(list_card)

    def create_form_field(self, parent, label, variable):
        container = ttk.Frame(parent, style='Card.TFrame')
        container.pack(fill='x', pady=5)
        
        ttk.Label(container,
                 text=f"{label} *",
                 style='Field.TLabel').pack(anchor='w', pady=(0, 5))
        
        entry = ttk.Entry(container,
                         textvariable=variable,
                         style='Custom.TEntry')
        entry.pack(fill='x')

    def create_datetime_selectors(self, parent):
        """Create date and time selection widgets"""
        # Date selector
        date_container = ttk.Frame(parent, style='Card.TFrame')
        date_container.pack(fill='x', pady=5)
        
        ttk.Label(date_container,
                 text="Tour Date *",
                 style='Field.TLabel').pack(anchor='w', pady=(0, 5))
        
        # Set minimum date to today
        min_date = datetime.now().date()
        
        self.date_picker = tkcalendar.DateEntry(
            date_container,
            width=20,
            background=self.colors['primary'],
            foreground='white',
            borderwidth=0,
            font=('Helvetica', 10),
            mindate=min_date,
            firstweekday='monday',  # Start calendar on Monday
            date_pattern='yyyy-mm-dd'
        )
        self.date_picker.pack(fill='x')
        
        # Time selector
        time_container = ttk.Frame(parent, style='Card.TFrame')
        time_container.pack(fill='x', pady=5)
        
        ttk.Label(time_container,
                 text="Tour Time *",
                 style='Field.TLabel').pack(anchor='w', pady=(0, 5))
        
        time_frame = ttk.Frame(time_container)
        time_frame.pack(fill='x')
        
        # Hour spinbox
        self.hour_var = tk.StringVar(value="09")  # Initialize with default value
        hour_spin = ttk.Spinbox(
            time_frame, 
            from_=1, 
            to=12, 
            width=3,
            textvariable=self.hour_var,
            format="%02.0f",
            wrap=True  # Allow wrapping around
        )
        hour_spin.pack(side='left')
        
        ttk.Label(time_frame, text=":").pack(side='left', padx=2)
        
        # Minute spinbox
        self.minute_var = tk.StringVar(value="00")  # Initialize with default value
        minute_spin = ttk.Spinbox(
            time_frame,
            from_=0,
            to=59,
            width=3,
            textvariable=self.minute_var,
            format="%02.0f",
            wrap=True
        )
        minute_spin.pack(side='left')
        
        # AM/PM selector
        self.ampm_var = tk.StringVar(value="AM")  # Initialize with default value
        ttk.Combobox(
            time_frame,
            values=('AM', 'PM'),
            width=3,
            textvariable=self.ampm_var,
            state='readonly'
        ).pack(side='left', padx=(5, 0))

    def refresh_tours(self):
        """Refresh the tours list"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            # Fetch tours
            tours = self.api_client.get_tours()
            
            # Sort tours by date/time
            sorted_tours = sorted(
                tours,
                key=lambda x: datetime.fromisoformat(x['tour_time'])
            )
            
            # Display tours
            for i, tour in enumerate(sorted_tours):
                tour_time = datetime.fromisoformat(tour['tour_time'])
                date_str = tour_time.strftime('%Y-%m-%d')
                time_str = tour_time.strftime('%I:%M %p')
                
                # Alternate row colors
                tag = 'oddrow' if i % 2 else ''
                
                self.tree.insert('', 'end', values=(
                    date_str,
                    time_str,
                    tour['client_name'],
                    tour.get('phone_number', 'N/A'),
                    tour['property_id']
                ), tags=(tag,))
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh tours: {str(e)}")

    def schedule_tour(self):
        """Handle tour scheduling"""
        if not self.validate_inputs():
            return
            
        try:
            # Parse time
            time_str = self.time_var.get()
            date = self.date_picker.get_date()
            
            # Validate tour time
            if not self.validate_tour_time(date, time_str):
                return
                
            # Parse time for API
            time_format = "%I:%M %p"
            parsed_time = datetime.strptime(time_str, time_format)
            
            # Combine date and time
            tour_time = datetime.combine(date, parsed_time.time())
            
            # Format client name
            client_name = f"{self.first_name_var.get().strip()} {self.last_name_var.get().strip()}"
            
            # Schedule the tour
            result = self.api_client.create_tour(
                property_id=self.property_id_var.get().strip(),
                tour_time=tour_time,
                client_name=client_name,
                phone_number=self.phone_var.get().strip()
            )

            if result:
                messagebox.showinfo("Success", "Tour scheduled successfully")
                self.clear_form()
                self.refresh_tours()
            else:
                messagebox.showerror("Error", "Unable to schedule tour. Please try again.")
                
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def validate_phone_number(self, phone):
        """Validate phone number format"""
        # Remove all non-numeric characters
        cleaned = ''.join(filter(str.isdigit, phone))
        
        # Check length
        if len(cleaned) != 10:
            return False
            
        # Format validation (XXX-XXX-XXXX)
        try:
            formatted = f"{cleaned[:3]}-{cleaned[3:6]}-{cleaned[6:]}"
            return True, formatted
        except:
            return False, None

    def validate_inputs(self):
        """Validate form inputs"""
        validation_fields = [
            (self.first_name_var.get().strip(), "First Name"),
            (self.last_name_var.get().strip(), "Last Name"),
            (self.property_id_var.get().strip(), "Property ID")
        ]
        
        for value, field_name in validation_fields:
            if not value:
                messagebox.showwarning("Missing Information", f"Please enter {field_name}")
                return False

        # Validate phone number
        phone = self.phone_var.get().strip()
        is_valid, formatted_phone = self.validate_phone_number(phone)
        if not is_valid:
            messagebox.showwarning(
                "Invalid Input", 
                "Please enter a valid 10-digit phone number\nExample: 555-555-5555"
            )
            return False
        
        # Update phone number with formatted version
        self.phone_var.set(formatted_phone)
        return True

    def clear_form(self):
        """Clear all form fields"""
        self.first_name_var.set("")
        self.last_name_var.set("")
        self.phone_var.set("")
        self.property_id_var.set("")
        self.time_var.set("09:00 AM")
        self.date_picker.set_date(datetime.now())

    def show_schedule_form(self):
        """Show the tour scheduling form"""
        # Clear content area
        for widget in self.content.winfo_children():
            widget.destroy()
            
        # Create form container
        form_container = ttk.Frame(self.content, style='Card.TFrame')
        form_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Form title
        ttk.Label(form_container, 
                 text="Schedule New Tour",
                 style='CardTitle.TLabel').pack(pady=20)
        
        # Initialize variables
        self.first_name_var = tk.StringVar()
        self.last_name_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.property_id_var = tk.StringVar()
        self.time_var = tk.StringVar(value="09:00 AM")
        
        # Create form fields
        fields_frame = ttk.Frame(form_container, style='Card.TFrame')
        fields_frame.pack(fill='x', padx=40)
        
        # Client Information
        ttk.Label(fields_frame, text="Client Information", 
                 font=('Helvetica', 12, 'bold')).pack(anchor='w', pady=(0,10))
        
        self.create_form_field(fields_frame, "First Name:", self.first_name_var)
        self.create_form_field(fields_frame, "Last Name:", self.last_name_var)
        self.create_form_field(fields_frame, "Phone:", self.phone_var)
        
        ttk.Separator(fields_frame, orient='horizontal').pack(fill='x', pady=20)
        
        # Tour Details
        ttk.Label(fields_frame, text="Tour Details", 
                 font=('Helvetica', 12, 'bold')).pack(anchor='w', pady=(0,10))
        
        self.create_form_field(fields_frame, "Property ID:", self.property_id_var)
        
        # Date picker
        date_frame = ttk.Frame(fields_frame)
        date_frame.pack(fill='x', pady=5)
        ttk.Label(date_frame, text="Tour Date:").pack(side='left')
        self.date_picker = tkcalendar.DateEntry(
            date_frame,
            width=20,
            background=self.colors['primary'],
            foreground='white',
            borderwidth=2,
            date_pattern='yyyy-mm-dd'
        )
        self.date_picker.pack(side='left', padx=(10, 0))
        
        # Time selection
        time_frame = ttk.Frame(fields_frame)
        time_frame.pack(fill='x', pady=5)
        self.setup_time_selection(time_frame)
        
        # Submit button
        ttk.Button(fields_frame, 
                  text="Schedule Tour",
                  style='Primary.TButton',
                  command=self.schedule_tour).pack(pady=30)

    def show_tours_list(self):
        """Show the list of scheduled tours"""
        # Clear content area
        for widget in self.content.winfo_children():
            widget.destroy()
            
        # Create list container
        list_container = ttk.Frame(self.content, style='Card.TFrame')
        list_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # List title and refresh button
        header_frame = ttk.Frame(list_container)
        header_frame.pack(fill='x', padx=20, pady=20)
        ttk.Label(header_frame, text="Scheduled Tours", 
                 style='CardTitle.TLabel').pack(side='left')
        ttk.Button(header_frame, text="↻ Refresh",
                  style='Primary.TButton',
                  command=self.refresh_tours).pack(side='right')
        
        # Create Treeview
        self.tree = ttk.Treeview(
            list_container,
            columns=('Date', 'Time', 'Name', 'Phone', 'Property'),
            show='headings',
            height=15
        )
        
        # Configure columns
        column_widths = {
            'Date': 100,
            'Time': 80,
            'Name': 150,
            'Phone': 120,
            'Property': 100
        }
        
        for col, width in column_widths.items():
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width)
        
        self.tree.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_container, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Load tours
        self.refresh_tours()

    def show_settings(self):
        """Show settings page"""
        # Clear content area
        for widget in self.content.winfo_children():
            widget.destroy()
            
        # Create settings container
        settings_container = ttk.Frame(self.content, style='Card.TFrame')
        settings_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        ttk.Label(settings_container, 
                 text="Settings",
                 style='CardTitle.TLabel').pack(pady=20)
        
        # Add settings options here
        ttk.Label(settings_container,
                 text="Settings page under construction",
                 foreground=self.colors['secondary']).pack(pady=20)

    def create_form_field(self, parent, label, variable):
        """Helper method to create consistent form fields"""
        frame = ttk.Frame(parent)
        frame.pack(fill='x', pady=5)
        ttk.Label(frame, text=label).pack(side='left')
        ttk.Entry(frame, textvariable=variable, width=30).pack(side='left', padx=(10, 0))

    def init_variables(self):
        """Initialize all tkinter variables"""
        self.first_name_var = tk.StringVar()
        self.last_name_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.property_id_var = tk.StringVar()
        self.time_var = tk.StringVar(value="09:00 AM")

    def create_tours_treeview(self, parent):
        # Create Treeview with modern style
        self.tree = ttk.Treeview(
            parent,
            columns=('Date', 'Time', 'Name', 'Phone', 'Property', 'Status'),
            show='headings',
            style='Modern.Treeview',
            height=12
        )
        
        # Configure columns
        columns = {
            'Date': ('Date', 120),
            'Time': ('Time', 100),
            'Name': ('Client Name', 200),
            'Phone': ('Phone', 150),
            'Property': ('Property ID', 150),
            'Status': ('Status', 100)
        }
        
        for col, (heading, width) in columns.items():
            self.tree.heading(col, text=heading)
            self.tree.column(col, width=width, anchor='w')
        
        # Add modern scrollbar
        scrollbar = ttk.Scrollbar(parent, orient='vertical', command=self.tree.yview)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y', padx=(10, 0))
        
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Configure row colors
        self.tree.tag_configure('oddrow', background=self.colors['row_alt'])
        
        self.refresh_tours()

        # Add right-click menu
        self.tour_menu = tk.Menu(self.root, tearoff=0)
        self.tour_menu.add_command(label="Complete Tour", command=self.complete_selected_tour)
        self.tour_menu.add_command(label="Cancel Tour", command=self.cancel_selected_tour)
        self.tour_menu.add_separator()
        self.tour_menu.add_command(label="Edit Tour", command=self.edit_selected_tour)
        
        # Bind right-click to show menu
        self.tree.bind("<Button-3>", self.show_tour_menu)

    def setup_cached_styles(self):
        """Cache common styles for reuse"""
        self.cached_styles.update({
            'common_padding': {'padx': 20, 'pady': 20},
            'form_style': {'relief': 'solid', 'borderwidth': 1},
            'button_style': {'font': ('Segoe UI', 11)}
        })

    def get_tour_id_from_selection(self, item):
        """Get tour ID from the selected item"""
        try:
            item_values = self.tree.item(item)['values']
            if not item_values:
                messagebox.showerror("Error", "Invalid selection")
                return None
                
            tour_data = self.api_client.get_tours()
            if not tour_data:
                messagebox.showerror("Error", "Failed to fetch tour data")
                return None
                
            for tour in tour_data:
                if (tour['tour_time'].split('T')[0] == item_values[0] and
                    tour['client_name'] == item_values[2] and
                    tour['property_id'] == item_values[4]):
                    return tour
        except Exception as e:
            print(f"Error getting tour ID: {e}")
            return None

    def show_tour_menu(self, event):
        """Show the context menu on right-click"""
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.tour_menu.post(event.x_root, event.y_root)

    def complete_selected_tour(self):
        """Mark the selected tour as completed"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a tour to complete")
            return
        
        tour_id = self.get_tour_id_from_selection(selected[0])
        if tour_id:
            if messagebox.askyesno("Confirm", "Mark this tour as completed?"):
                if self.api_client.complete_tour(tour_id):
                    self.refresh_tours()
                    messagebox.showinfo("Success", "Tour marked as completed")
                else:
                    messagebox.showerror("Error", "Failed to complete tour")

    def cancel_selected_tour(self):
        """Cancel the selected tour"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a tour to cancel")
            return
        
        tour_id = self.get_tour_id_from_selection(selected[0])
        if tour_id:
            if messagebox.askyesno("Confirm", "Are you sure you want to cancel this tour?"):
                if self.api_client.cancel_tour(tour_id):
                    self.tree.selection_remove(selected)  # Clear selection
                    self.refresh_tours()
                    messagebox.showinfo("Success", "Tour cancelled")
                else:
                    messagebox.showerror("Error", "Failed to cancel tour")

    def edit_selected_tour(self):
        """Edit the selected tour"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a tour to edit")
            return
        
        tour_id = self.get_tour_id_from_selection(selected[0])
        if tour_id:
            # Create edit dialog
            EditTourDialog(self.root, self.api_client, tour_id, self.refresh_tours)

    def validate_tour_time(self, date, time_str):
        """Validate tour time against business rules"""
        try:
            # Parse time
            parsed_time = datetime.strptime(time_str, "%I:%M %p")
            hour = parsed_time.hour
            
            # Create full datetime
            tour_datetime = datetime.combine(date, parsed_time.time())
            current_time = datetime.now()

            # Check if date is in the future
            if tour_datetime <= current_time:
                messagebox.showerror("Invalid Time", "Please select a future date and time.")
                return False

            # Check if it's a weekday
            if tour_datetime.weekday() >= 5:  # 5 = Saturday, 6 = Sunday
                messagebox.showerror("Invalid Day", "Tours can only be scheduled Monday through Friday.")
                return False

            # Check business hours (9 AM - 5 PM)
            if hour < self.business_hours['start'] or hour >= self.business_hours['end']:
                messagebox.showerror(
                    "Invalid Time", 
                    "Tours can only be scheduled between 9:00 AM and 5:00 PM."
                )
                return False

            # Check lunch hour (12 PM - 1 PM)
            if self.business_hours['lunch_start'] <= hour < self.business_hours['lunch_end']:
                messagebox.showerror(
                    "Invalid Time",
                    "Tours cannot be scheduled during lunch hour (12:00 PM - 1:00 PM)."
                )
                return False

            return True
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid time format: {str(e)}")
            return False

    def get_available_times(self):
        """Generate list of available appointment times"""
        times = []
        for hour in range(self.business_hours['start'], self.business_hours['end']):
            # Skip lunch hour
            if hour >= self.business_hours['lunch_start'] and hour < self.business_hours['lunch_end']:
                continue
                
            # Convert to 12-hour format
            if hour == 12:
                times.append(f"12:00 PM")
            elif hour > 12:
                times.append(f"{hour-12:02d}:00 PM")
            else:
                times.append(f"{hour:02d}:00 AM")
        return times

    def setup_ui(self):
        """Setup the main UI"""
        # Remove duplicate date picker creation
        self.create_form_fields()
        self.create_datetime_selectors(self.form_frame)
        self.create_buttons()
        self.create_tour_list()