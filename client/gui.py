import tkinter as tk
from tkinter import ttk, messagebox
import tkcalendar
from datetime import datetime
from api_client import TourAPIClient
from config import validate_config

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
        
        # Configure styles
        self.setup_styles()
        self.init_variables()
        self.create_layout()

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
        # Date selector
        date_container = ttk.Frame(parent, style='Card.TFrame')
        date_container.pack(fill='x', pady=5)
        
        ttk.Label(date_container,
                 text="Tour Date *",
                 style='Field.TLabel').pack(anchor='w', pady=(0, 5))
        
        self.date_picker = tkcalendar.DateEntry(
            date_container,
            width=20,
            background=self.colors['primary'],
            foreground='white',
            borderwidth=0,
            font=('Helvetica', 10)
        )
        self.date_picker.pack(fill='x')
        
        # Time selector
        time_container = ttk.Frame(parent, style='Card.TFrame')
        time_container.pack(fill='x', pady=5)
        
        ttk.Label(time_container,
                 text="Tour Time *",
                 style='Field.TLabel').pack(anchor='w', pady=(0, 5))
        
        times = [f"{h:02d}:00 {ap}" for h in range(9, 18) for ap in ('AM', 'PM')]
        self.time_combo = ttk.Combobox(
            time_container,
            textvariable=self.time_var,
            values=times,
            state='readonly',
            font=('Helvetica', 10)
        )
        self.time_combo.pack(fill='x')

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
            time_format = "%I:%M %p"
            parsed_time = datetime.strptime(time_str, time_format)
            
            # Combine date and time
            date = self.date_picker.get_date()
            tour_time = datetime.combine(date, parsed_time.time())
            
            # Format client name
            client_name = f"{self.first_name_var.get().strip()} {self.last_name_var.get().strip()}"
            
            # Schedule the tour
            result = self.api_client.create_tour(
                property_id=self.property_id_var.get().strip(),
                tour_time=tour_time.isoformat(),
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

    def validate_inputs(self):
        """Validate form inputs"""
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
            messagebox.showwarning(
                "Invalid Input", 
                "Please enter a valid 10-digit phone number\nExample: 555-555-5555"
            )
            return False
            
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
        ttk.Label(time_frame, text="Tour Time:").pack(side='left')
        times = [f"{h:02d}:00 {ap}" for h in range(9, 18) for ap in ('AM', 'PM')]
        self.time_combo = ttk.Combobox(
            time_frame,
            textvariable=self.time_var,
            values=times,
            state='readonly',
            width=18
        )
        self.time_combo.pack(side='left', padx=(10, 0))
        
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
            columns=('Date', 'Time', 'Name', 'Phone', 'Property'),
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
            'Property': ('Property ID', 150)
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