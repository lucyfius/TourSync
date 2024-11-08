import tkinter as tk
from tkinter import ttk
from api_client import TourAPIClient
from datetime import datetime
from tkcalendar import DateEntry
from PIL import Image, ImageTk
import os
from tkinter import messagebox

class ModernUI(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.api_client = TourAPIClient()
        
        # Initialize colors first
        self.colors = {
            'bg': '#F8FAFC',           # Background
            'sidebar': '#1E293B',       # Dark sidebar
            'sidebar_hover': '#334155', 
            'sidebar_active': '#2563EB',
            'white': '#FFFFFF',         # Card background
            'text': '#0F172A',          # Headers
            'text_secondary': '#475569', # Labels
            'text_light': '#E2E8F0',    # Light text for sidebar
            'border': '#E2E8F0',        # Subtle borders
            'primary': '#2563EB',       # Primary action
            'primary_hover': '#1D4ED8',
            'success': '#059669',
            'error': '#DC2626'
        }
        
        # Initialize variables
        self.init_variables()
        
        # Setup UI components
        self.setup_styles()
        self.create_layout()
        
    def init_variables(self):
        """Initialize all necessary variables"""
        self.tours = []
        self.selected_tour = None
        self.property_var = tk.StringVar()
        self.client_name_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.time_var = tk.StringVar()
        
    def setup_styles(self):
        """Setup sophisticated UI styles"""
        self.style = ttk.Style()
        
        # Enhanced color scheme
        self.colors = {
            'bg': '#F8FAFC',           # Background
            'sidebar': '#1E293B',       # Dark sidebar
            'sidebar_hover': '#334155', 
            'sidebar_active': '#2563EB',
            'white': '#FFFFFF',         # Card background
            'text': '#0F172A',          # Headers
            'text_secondary': '#475569', # Labels
            'text_light': '#E2E8F0',    # Light text for sidebar
            'border': '#E2E8F0',        # Subtle borders
            'primary': '#2563EB',       # Primary action
            'primary_hover': '#1D4ED8',
            'success': '#059669',
            'error': '#DC2626'
        }

        # Frame styles
        self.style.configure('Card.TFrame',
                            background=self.colors['white'],
                            relief='flat')

        # Typography
        self.style.configure('Header.TLabel',
                            background=self.colors['white'],
                            foreground=self.colors['text'],
                            font=('Segoe UI', 28, 'bold'))
                        
        self.style.configure('SubHeader.TLabel',
                            background=self.colors['white'],
                            foreground=self.colors['text'],
                            font=('Segoe UI', 20, 'bold'))

        self.style.configure('FieldLabel.TLabel',
                            background=self.colors['white'],
                            foreground=self.colors['text_secondary'],
                            font=('Segoe UI', 12))

        # Modern entry style
        self.style.configure('Modern.TEntry',
                            fieldbackground=self.colors['white'],
                            bordercolor=self.colors['border'],
                            borderwidth=1,
                            relief='solid',
                            padding=10)

        # Configure focused entry style
        self.style.map('Modern.TEntry',
                       bordercolor=[('focus', self.colors['primary'])],
                       lightcolor=[('focus', self.colors['primary'])],
                       darkcolor=[('focus', self.colors['primary'])])

        # Button styles
        self.style.configure('Primary.TButton',
                            font=('Segoe UI', 12, 'bold'),
                            background=self.colors['primary'],
                            foreground='white',
                            padding=(20, 12),
                            borderwidth=0,
                            relief='flat')
                        
        self.style.map('Primary.TButton',
                       background=[('active', self.colors['primary_hover'])])

        # Sidebar styles
        self.style.configure('Sidebar.TFrame',
                            background=self.colors['sidebar'])
                        
        self.style.configure('SidebarItem.TLabel',
                            background=self.colors['sidebar'],
                            foreground=self.colors['white'],
                            font=('Segoe UI', 13))

    def create_layout(self):
        """Create main application layout"""
        # Main container
        self.main_container = tk.Frame(self, bg=self.colors['bg'])
        self.main_container.pack(fill='both', expand=True)
        
        # Create sidebar first and fix its width
        self.create_sidebar()
        
        # Create content area
        self.content = tk.Frame(self.main_container, bg=self.colors['bg'])
        self.content.pack(side='left', fill='both', expand=True)
        
        # Create main content
        self.create_content()

    def create_sidebar(self):
        """Create modern sidebar with icons"""
        # Fixed width sidebar
        self.sidebar = tk.Frame(self.main_container, bg=self.colors['sidebar'], width=250)
        self.sidebar.pack(side='left', fill='y')
        self.sidebar.pack_propagate(False)  # Prevent sidebar from shrinking
        
        # App title
        title_frame = tk.Frame(self.sidebar, bg=self.colors['sidebar'])
        title_frame.pack(fill='x', pady=(25, 40), padx=25)
        
        tk.Label(title_frame,
                text="TourSync",
                font=('Segoe UI', 24, 'bold'),
                fg=self.colors['text_light'],
                bg=self.colors['sidebar']).pack(anchor='w')

        # Navigation items with icons and commands
        nav_items = [
            ('Dashboard', '📊', self.show_dashboard),
            ('Tours', '🗓️', self.show_tours),
            ('Properties', '🏠', self.show_properties),
            ('Reports', '📈', self.show_reports),
            ('Settings', '⚙️', self.show_settings)
        ]
        
        for text, icon, command in nav_items:
            self.create_nav_item(text, icon, command)

    def create_nav_item(self, text, icon, command):
        """Create polished navigation item with functionality"""
        frame = tk.Frame(self.sidebar, bg=self.colors['sidebar'])
        frame.pack(fill='x', pady=2)
        
        # Content container with padding
        content = tk.Frame(frame, bg=self.colors['sidebar'])
        content.pack(fill='x', padx=(25, 20), pady=12)
        
        # Icon and text
        icon_label = tk.Label(content,
                             text=icon,
                             font=('Segoe UI', 16),
                             fg=self.colors['text_light'],
                             bg=self.colors['sidebar'])
        icon_label.pack(side='left', padx=(0, 12))
        
        text_label = tk.Label(content,
                             text=text,
                             font=('Segoe UI', 13),
                             fg=self.colors['text_light'],
                             bg=self.colors['sidebar'])
        text_label.pack(side='left')
        
        # Bind click event
        for widget in [frame, content, icon_label, text_label]:
            widget.bind('<Button-1>', lambda e: command())
        
        # Hover effects
        def on_enter(e):
            frame.configure(bg=self.colors['sidebar_hover'])
            content.configure(bg=self.colors['sidebar_hover'])
            icon_label.configure(bg=self.colors['sidebar_hover'])
            text_label.configure(bg=self.colors['sidebar_hover'])
                
        def on_leave(e):
            frame.configure(bg=self.colors['sidebar'])
            content.configure(bg=self.colors['sidebar'])
            icon_label.configure(bg=self.colors['sidebar'])
            text_label.configure(bg=self.colors['sidebar'])
        
        for widget in [frame, content, icon_label, text_label]:
            widget.bind('<Enter>', on_enter)
            widget.bind('<Leave>', on_leave)

    # Navigation functions
    def show_dashboard(self):
        """Show dashboard with all tours"""
        self.clear_content()
        
        # Main container
        container = tk.Frame(self.content, bg=self.colors['white'])
        container.pack(fill='both', expand=True, padx=40, pady=30)
        
        # Header
        header = tk.Frame(container, bg=self.colors['white'])
        header.pack(fill='x', pady=(0, 30))
        
        tk.Label(header,
                text="Dashboard",
                font=('Segoe UI', 28, 'bold'),
                fg=self.colors['text'],
                bg=self.colors['white']).pack(side='left')
        
        ttk.Button(header,
                  text="↻ Refresh",
                  style='Secondary.TButton',
                  command=lambda: self.show_dashboard()).pack(side='right')
        
        # Create scrollable frame for tours
        tours_frame = tk.Frame(container, bg=self.colors['white'])
        tours_frame.pack(fill='both', expand=True)
        
        # Display tours in the frame
        self.display_tours(tours_frame)

    def show_tours(self):
        """Show tours view"""
        self.clear_content()
        self.create_content()  # This shows the tours/schedule view

    def show_properties(self):
        """Show properties management interface"""
        self.clear_content()
        
        # Main container
        container = tk.Frame(self.content, bg=self.colors['white'])
        container.pack(fill='both', expand=True, padx=40, pady=30)
        
        # Header with add property button
        header_frame = tk.Frame(container, bg=self.colors['white'])
        header_frame.pack(fill='x', pady=(0, 30))
        
        tk.Label(header_frame,
                text="Properties",
                font=('Segoe UI', 28, 'bold'),
                fg=self.colors['text'],
                bg=self.colors['white']).pack(side='left')
                
        ttk.Button(header_frame,
                  text="+ Add Property",
                  style='Primary.TButton',
                  command=self.show_add_property_dialog).pack(side='right')
        
        # Properties list container with scrollbar
        list_frame = tk.Frame(container, bg=self.colors['white'])
        list_frame.pack(fill='both', expand=True)
        
        # Create canvas for scrolling
        canvas = tk.Canvas(list_frame, bg=self.colors['white'])
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
        self.properties_frame = tk.Frame(canvas, bg=self.colors['white'])
        
        # Configure canvas
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack scrollbar and canvas
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        
        # Create window in canvas
        canvas_frame = canvas.create_window((0, 0), window=self.properties_frame, anchor="nw")
        
        # Configure canvas scrolling
        def configure_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        self.properties_frame.bind('<Configure>', configure_scroll_region)
        
        # Load properties
        self.load_properties()

    def load_properties(self):
        """Load and display properties"""
        # Clear existing properties
        for widget in self.properties_frame.winfo_children():
            widget.destroy()
            
        properties = self.api_client.get_properties()
        
        if not properties:
            ttk.Label(self.properties_frame,
                     text="No properties found",
                     style='FormLabel.TLabel').pack(pady=20)
            return
            
        # Display properties
        for prop in properties:
            self.create_property_card(self.properties_frame, prop)

    def show_reports(self):
        """Show reports view"""
        self.clear_content()
        
        # Main container for reports
        container = tk.Frame(self.content, bg=self.colors['white'])
        container.pack(fill='both', expand=True, padx=40, pady=30)
        
        # Header
        tk.Label(container,
                text="Reports",
                font=('Segoe UI', 28, 'bold'),
                fg=self.colors['text'],
                bg=self.colors['white']).pack(anchor='w', pady=(0, 30))
        
        # Reports options
        reports = [
            ("Tour Activity", "View tour statistics and trends"),
            ("Property Performance", "Analyze property viewing metrics"),
            ("Client Analytics", "Review client engagement data")
        ]
        
        for title, description in reports:
            self.create_report_card(container, title, description)

    def show_settings(self):
        """Show settings view"""
        self.clear_content()
        
        # Main container for settings
        container = tk.Frame(self.content, bg=self.colors['white'])
        container.pack(fill='both', expand=True, padx=40, pady=30)
        
        # Header
        tk.Label(container,
                text="Settings",
                font=('Segoe UI', 28, 'bold'),
                fg=self.colors['text'],
                bg=self.colors['white']).pack(anchor='w', pady=(0, 30))
        
        # Settings sections
        settings = [
            ("Profile", "Manage your account information"),
            ("Notifications", "Configure alert preferences"),
            ("API Settings", "Manage API keys and endpoints"),
            ("Theme", "Customize application appearance")
        ]
        
        for title, description in settings:
            self.create_settings_card(container, title, description)

    def clear_content(self):
        """Clear current content"""
        for widget in self.content.winfo_children():
            widget.destroy()

    def create_content(self):
        """Create refined content area"""
        # Main content container with padding
        content_frame = ttk.Frame(self.content, style='Main.TFrame')
        content_frame.pack(fill='both', expand=True, padx=40, pady=30)
        
        # Schedule Tour card
        schedule_card = ttk.Frame(content_frame, style='Card.TFrame')
        schedule_card.pack(fill='x', padx=2, pady=2)
        
        # Add subtle shadow effect
        self.add_shadow(schedule_card)
        
        # Create schedule form
        self.create_schedule_section(schedule_card)
        
        # Upcoming Tours card
        tours_card = ttk.Frame(content_frame, style='Card.TFrame')
        tours_card.pack(fill='both', expand=True, padx=2, pady=(30, 2))
        
        # Add subtle shadow effect
        self.add_shadow(tours_card)
        
        # Create tours section
        self.create_tours_section(tours_card)

    def create_schedule_section(self, parent):
        """Create polished schedule form section"""
        container = ttk.Frame(parent, style='Card.TFrame')
        container.pack(fill='both', expand=True, padx=40, pady=30)
        
        # Section header
        ttk.Label(container,
                 text="Schedule Tour",
                 style='Header.TLabel').pack(anchor='w', pady=(0, 40))
        
        # Form grid
        form_grid = ttk.Frame(container, style='Card.TFrame')
        form_grid.pack(fill='x', pady=(0, 30))
        
        # Form fields with consistent spacing
        fields = [
            ("Property ID", self.property_var),
            ("Client Name", self.client_name_var),
            ("Phone Number", self.phone_var)
        ]
        
        for label, var in fields:
            self.create_form_field(form_grid, label, var)
        
        # Date and time container
        datetime_frame = ttk.Frame(form_grid, style='Card.TFrame')
        datetime_frame.pack(fill='x', pady=(0, 20))
        
        # Modern date picker
        date_container = ttk.Frame(datetime_frame, style='Card.TFrame')
        date_container.pack(fill='x', pady=(0, 15))
        
        ttk.Label(date_container,
                 text="Date",
                 style='FieldLabel.TLabel').pack(anchor='w', pady=(0, 8))
                 
        self.date_picker = DateEntry(
            date_container,
            width=30,
            font=('Segoe UI', 12),
            borderwidth=0,
            background=self.colors['white'],
            foreground=self.colors['text'],
            selectbackground=self.colors['primary'],
            selectforeground=self.colors['white']
        )
        self.date_picker.pack(fill='x')
        
        # Time field
        self.create_form_field(form_grid, "Time (HH:MM)", self.time_var)
        
        # Button container
        button_container = ttk.Frame(form_grid, style='Card.TFrame')
        button_container.pack(fill='x', pady=(20, 0))
        
        ttk.Button(button_container,
                  text="Schedule Tour →",
                  style='Primary.TButton',
                  command=self.submit_tour).pack(side='right')

    def create_form_field(self, parent, label, variable):
        """Create sophisticated form field"""
        container = tk.Frame(parent, bg=self.colors['white'])
        container.pack(fill='x', pady=(0, 20))
        
        # Label
        label_widget = tk.Label(container,
                               text=label,
                               font=('Segoe UI', 12),
                               fg=self.colors['text_secondary'],
                               bg=self.colors['white'])
        label_widget.pack(anchor='w', pady=(0, 5))
        
        # Entry with modern styling
        entry = ttk.Entry(container,
                         textvariable=variable,
                         style='Modern.TEntry')
        entry.pack(fill='x')
        
        # Focus effects
        def on_focus_in(e):
            label_widget.configure(fg=self.colors['primary'])
        
        def on_focus_out(e):
            label_widget.configure(fg=self.colors['text_secondary'])
        
        entry.bind('<FocusIn>', on_focus_in)
        entry.bind('<FocusOut>', on_focus_out)
        
        return entry

    def on_nav_hover(self, event, frame):
        """Handle navigation item hover effect"""
        if event.type == '7': # Enter
            frame.configure(style='SidebarHover.TFrame')
        else: # Leave
            frame.configure(style='Sidebar.TFrame')

    def submit_tour(self):
        """Handle tour submission"""
        try:
            # Get form values
            property_id = self.property_var.get().strip()
            client_name = self.client_name_var.get().strip()
            phone_number = self.phone_var.get().strip()
            date = self.date_picker.get_date()
            time = self.time_var.get().strip()

            # Validate inputs
            if not all([property_id, client_name, phone_number, time]):
                messagebox.showerror("Error", "All fields are required")
                return

            # Create datetime
            try:
                hour, minute = map(int, time.split(':'))
                tour_datetime = datetime.combine(date, datetime.min.time().replace(hour=hour, minute=minute))
            except ValueError:
                messagebox.showerror("Error", "Invalid time format. Use HH:MM")
                return

            # Submit to API
            response = self.api_client.create_tour(
                property_id=property_id,
                tour_time=tour_datetime,
                client_name=client_name,
                phone_number=phone_number
            )

            if response:
                messagebox.showinfo("Success", "Tour scheduled successfully!")
                self.clear_form()
                self.load_tours()
            else:
                messagebox.showerror("Error", "Failed to schedule tour")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def clear_form(self):
        """Clear all form fields"""
        self.property_var.set("")
        self.client_name_var.set("")
        self.phone_var.set("")
        self.time_var.set("")
        self.date_picker.set_date(datetime.now())

    def load_tours(self):
        """Load and display tours"""
        try:
            # Clear existing tours
            for widget in self.tours_list.winfo_children():
                widget.destroy()
            
            # Get tours from API
            tours = self.api_client.get_tours()
            
            if not tours:
                ttk.Label(self.tours_list,
                         text="No tours scheduled",
                         style='FormLabel.TLabel').pack(pady=20)
                return
            
            # Sort tours by date and time
            tours.sort(key=lambda x: (x['date'], x['time']))
            
            # Display tours
            for tour in tours:
                self.create_tour_card(self.tours_list, tour)
                
        except Exception as e:
            print(f"Failed to load tours: {str(e)}")
            error_frame = ttk.Frame(self.tours_list)
            error_frame.pack(fill='x', pady=20)
            
            ttk.Label(error_frame,
                     text="⚠️ Unable to load tours",
                     style='Error.TLabel').pack(anchor='w')
                     
            ttk.Label(error_frame,
                     text="Please check your connection and try again.",
                     style='FormLabel.TLabel').pack(anchor='w', pady=(5, 10))
                     
            ttk.Button(error_frame,
                      text="Try Again",
                      style='Primary.TButton',
                      command=self.refresh_dashboard).pack(anchor='w')

    def create_tours_section(self, parent):
        """Create tours section with scrollable list"""
        # Section header
        header_frame = ttk.Frame(parent, style='Card.TFrame')
        header_frame.pack(fill='x', padx=30, pady=(30, 20))
        
        ttk.Label(header_frame,
                 text="Upcoming Tours",
                 style='Header.TLabel').pack(side='left')
        
        # Create scrollable frame
        container = ttk.Frame(parent, style='Card.TFrame')
        container.pack(fill='both', expand=True, padx=30, pady=(0, 30))
        
        # Add scrollbar
        canvas = tk.Canvas(container, bg=self.colors['white'])
        scrollbar = ttk.Scrollbar(container, orient='vertical', command=canvas.yview)
        
        # Create frame for tours and assign it to self.tours_list
        self.tours_list = ttk.Frame(canvas, style='Card.TFrame')
        self.tours_list.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        
        canvas.create_window((0, 0), window=self.tours_list, anchor='nw', width=canvas.winfo_width())
        canvas.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side='right', fill='y')
        canvas.pack(side='left', fill='both', expand=True)
        
        # Load tours
        self.display_tours(self.tours_list)  # Changed from tours_frame to self.tours_list

    def create_tour_card(self, parent, tour):
        """Create individual tour card"""
        try:
            card = tk.Frame(parent, bg=self.colors['white'], relief='solid', borderwidth=1)
            card.pack(fill='x', pady=8, padx=2)
            
            content = tk.Frame(card, bg=self.colors['white'])
            content.pack(fill='x', padx=20, pady=15)
            
            # Date and time
            tk.Label(content,
                    text=f"📅 {tour.get('date', 'N/A')} at {tour.get('time', 'N/A')}",
                    font=('Segoe UI', 14, 'bold'),
                    fg=self.colors['text'],
                    bg=self.colors['white']).pack(anchor='w')
            
            # Property address
            tk.Label(content,
                    text=f"🏠 {tour.get('property_address', tour.get('property_id', 'N/A'))}",
                    font=('Segoe UI', 12),
                    fg=self.colors['text_secondary'],
                    bg=self.colors['white']).pack(anchor='w', pady=(10, 0))
            
            # Client info
            tk.Label(content,
                    text=f"👤 {tour.get('client_name', 'N/A')}",
                    font=('Segoe UI', 12),
                    fg=self.colors['text_secondary'],
                    bg=self.colors['white']).pack(anchor='w', pady=(5, 0))
            
            # Phone number
            tk.Label(content,
                    text=f"📱 {tour.get('phone_number', 'N/A')}",
                    font=('Segoe UI', 12),
                    fg=self.colors['text_secondary'],
                    bg=self.colors['white']).pack(anchor='w', pady=(5, 0))
            
            # Cancel button
            ttk.Button(content,
                      text="Cancel Tour",
                      style='Danger.TButton',
                      command=lambda: self.cancel_tour(tour['id'])).pack(anchor='w', pady=(15, 0))
                  
        except Exception as e:
            print(f"Error creating tour card: {str(e)}")

    def add_shadow(self, widget):
        """Add subtle shadow effect to widgets"""
        shadow = ttk.Frame(widget.master)
        shadow.place(in_=widget, x=2, y=2, relwidth=1, relheight=1)
        shadow.lower(widget)

    def create_property_list(self, parent, properties):
        """Create property cards"""
        for prop in properties:
            # Property card
            card = tk.Frame(parent, bg=self.colors['white'], relief='solid', borderwidth=1)
            card.pack(fill='x', pady=8, padx=2)
            
            # Property info
            info_frame = tk.Frame(card, bg=self.colors['white'])
            info_frame.pack(fill='x', padx=20, pady=15)
            
            tk.Label(info_frame,
                    text=f"Property {prop['id']}",
                    font=('Segoe UI', 14, 'bold'),
                    fg=self.colors['text'],
                    bg=self.colors['white']).pack(anchor='w')
                    
            tk.Label(info_frame,
                    text=prop['address'],
                    font=('Segoe UI', 12),
                    fg=self.colors['text_secondary'],
                    bg=self.colors['white']).pack(anchor='w', pady=(5, 0))
                    
            tk.Label(info_frame,
                    text=prop['type'],
                    font=('Segoe UI', 12),
                    fg=self.colors['text_secondary'],
                    bg=self.colors['white']).pack(anchor='w', pady=(5, 0))

    def create_report_card(self, parent, title, description):
        """Create report option card"""
        card = tk.Frame(parent, bg=self.colors['white'], relief='solid', borderwidth=1)
        card.pack(fill='x', pady=8, padx=2)
        
        content = tk.Frame(card, bg=self.colors['white'])
        content.pack(fill='x', padx=20, pady=15)
        
        tk.Label(content,
                text=title,
                font=('Segoe UI', 14, 'bold'),
                fg=self.colors['text'],
                bg=self.colors['white']).pack(anchor='w')
                
        tk.Label(content,
                text=description,
                font=('Segoe UI', 12),
                fg=self.colors['text_secondary'],
                bg=self.colors['white']).pack(anchor='w', pady=(5, 0))
        
        ttk.Button(content,
                  text="Generate Report",
                  style='Primary.TButton',
                  command=lambda t=title: self.generate_report(t)).pack(anchor='w', pady=(15, 0))

    def create_settings_card(self, parent, title, description):
        """Create settings option card"""
        card = tk.Frame(parent, bg=self.colors['white'], relief='solid', borderwidth=1)
        card.pack(fill='x', pady=8, padx=2)
        
        content = tk.Frame(card, bg=self.colors['white'])
        content.pack(fill='x', padx=20, pady=15)
        
        tk.Label(content,
                text=title,
                font=('Segoe UI', 14, 'bold'),
                fg=self.colors['text'],
                bg=self.colors['white']).pack(anchor='w')
                
        tk.Label(content,
                text=description,
                font=('Segoe UI', 12),
                fg=self.colors['text_secondary'],
                bg=self.colors['white']).pack(anchor='w', pady=(5, 0))
        
        ttk.Button(content,
                  text="Configure",
                  style='Primary.TButton',
                  command=lambda t=title: self.configure_setting(t)).pack(anchor='w', pady=(15, 0))

    def generate_report(self, report_type):
        """Handle report generation"""
        messagebox.showinfo("Generate Report", f"Generating {report_type} report...")

    def configure_setting(self, setting_type):
        """Handle settings configuration"""
        messagebox.showinfo("Configure Settings", f"Configuring {setting_type}...")

    def show_add_property_dialog(self):
        """Show dialog to add new property"""
        dialog = tk.Toplevel(self)
        dialog.title("Add New Property")
        dialog.geometry("400x200")  # Smaller size since we only need one field
        dialog.configure(bg=self.colors['white'])
        
        # Center the dialog
        dialog.transient(self)
        dialog.grab_set()
        
        # Form container
        form_frame = tk.Frame(dialog, bg=self.colors['white'])
        form_frame.pack(fill='both', expand=True, padx=30, pady=20)
        
        # Property Address field
        tk.Label(form_frame,
                text="Property Address",
                font=('Segoe UI', 12),
                fg=self.colors['text'],
                bg=self.colors['white']).pack(anchor='w', pady=(0, 5))
                
        address_var = tk.StringVar()
        address_entry = ttk.Entry(form_frame,
                                textvariable=address_var,
                                font=('Segoe UI', 12))
        address_entry.pack(fill='x', pady=(0, 20))
        
        # Buttons
        button_frame = tk.Frame(form_frame, bg=self.colors['white'])
        button_frame.pack(fill='x', pady=(10, 0))
        
        ttk.Button(button_frame,
                  text="Cancel",
                  style='Secondary.TButton',
                  command=dialog.destroy).pack(side='right', padx=(10, 0))
                  
        ttk.Button(button_frame,
                  text="Add Property",
                  style='Primary.TButton',
                  command=lambda: self.add_property(address_var.get(), dialog)).pack(side='right')

    def add_property(self, address, dialog):
        """Add new property"""
        if not address.strip():
            messagebox.showerror("Error", "Property address is required")
            return
        
        try:
            # Create property data (simplified)
            property_data = {
                'address': address.strip()
            }
            
            # Add to database through API
            response = self.api_client.add_property(property_data)
            if response:
                messagebox.showinfo("Success", "Property added successfully!")
                dialog.destroy()
                self.load_properties()  # Refresh property list
            else:
                messagebox.showerror("Error", "Failed to add property")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def edit_property(self, property_id):
        """Show dialog to edit property"""
        # Similar to add_property_dialog but pre-filled with existing data
        property_data = self.api_client.get_property(property_id)
        if not property_data:
            messagebox.showerror("Error", "Failed to load property data")
            return
        
        # Show edit dialog with pre-filled data
        # Similar structure to add_property_dialog
        ...

    def delete_property(self, property_id):
        """Delete property after confirmation"""
        if messagebox.askyesno("Confirm Delete", 
                              "Are you sure you want to delete this property? This cannot be undone."):
            try:
                response = self.api_client.delete_property(property_id)
                if response:
                    messagebox.showinfo("Success", "Property deleted successfully!")
                    self.load_properties()  # Refresh list
                else:
                    messagebox.showerror("Error", "Failed to delete property")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def create_property_card(self, parent, prop):
        """Create individual property card"""
        card = tk.Frame(parent, bg=self.colors['white'], relief='solid', borderwidth=1)
        card.pack(fill='x', pady=8, padx=2)
        
        content = tk.Frame(card, bg=self.colors['white'])
        content.pack(fill='x', padx=20, pady=15)
        
        # Property address
        tk.Label(content,
                text=prop['address'],
                font=('Segoe UI', 14),
                fg=self.colors['text'],
                bg=self.colors['white']).pack(anchor='w')
        
        # Action buttons
        button_frame = tk.Frame(content, bg=self.colors['white'])
        button_frame.pack(fill='x', pady=(15, 0))
        
        ttk.Button(button_frame,
                  text="Delete",
                  style='Danger.TButton',
                  command=lambda p=prop['id']: self.delete_property(p)).pack(side='left')

    def refresh_dashboard(self):
        """Refresh the dashboard"""
        self.show_dashboard()

    def display_tours(self, parent_frame):
        """Display tours in the given frame"""
        try:
            # Get tours from API
            tours = self.api_client.get_tours()
            
            if not tours:
                tk.Label(parent_frame,
                        text="No tours scheduled",
                        font=('Segoe UI', 12),
                        fg=self.colors['text_secondary'],
                        bg=self.colors['white']).pack(pady=20)
                return
                
            # Sort tours by date and time
            tours.sort(key=lambda x: (x['date'], x['time']))
            
            # Display tours
            for tour in tours:
                self.create_tour_card(parent_frame, tour)
                
        except Exception as e:
            print(f"Failed to load tours: {str(e)}")
            error_frame = tk.Frame(parent_frame, bg=self.colors['white'])
            error_frame.pack(fill='x', pady=20)
            
            tk.Label(error_frame,
                    text="⚠️ Unable to load tours",
                    font=('Segoe UI', 12),
                    fg='red',
                    bg=self.colors['white']).pack(anchor='w')
                    
            tk.Label(error_frame,
                    text="Please check your connection and try again.",
                    font=('Segoe UI', 12),
                    fg=self.colors['text_secondary'],
                    bg=self.colors['white']).pack(anchor='w', pady=(5, 10))
                    
            ttk.Button(error_frame,
                      text="Try Again",
                      style='Primary.TButton',
                      command=self.refresh_view).pack(anchor='w')
            
            print(f"Error displaying tours: {str(e)}")

    def edit_tour(self, tour_id):
        """Edit existing tour"""
        messagebox.showinfo("Edit Tour", f"Editing tour {tour_id}")
        # Add edit tour functionality here

    def cancel_tour(self, tour_id):
        """Cancel a tour"""
        if messagebox.askyesno("Cancel Tour", "Are you sure you want to cancel this tour?"):
            try:
                if self.api_client.delete_tour(tour_id):
                    messagebox.showinfo("Success", "Tour cancelled successfully!")
                    self.refresh_view()
                else:
                    messagebox.showerror("Error", "Failed to cancel tour")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def create_tour(self, property_id):
        """Show dialog to create a new tour"""
        dialog = tk.Toplevel(self)
        dialog.title("Schedule Tour")
        dialog.geometry("400x400")
        dialog.configure(bg=self.colors['white'])
        
        # Center the dialog
        dialog.transient(self)
        dialog.grab_set()
        
        # Form container
        form_frame = tk.Frame(dialog, bg=self.colors['white'])
        form_frame.pack(fill='both', expand=True, padx=30, pady=20)
        
        # Client Name
        tk.Label(form_frame,
                text="Client Name",
                font=('Segoe UI', 12),
                fg=self.colors['text'],
                bg=self.colors['white']).pack(anchor='w', pady=(0, 5))
                
        client_name_var = tk.StringVar()
        ttk.Entry(form_frame,
                 textvariable=client_name_var,
                 font=('Segoe UI', 12)).pack(fill='x', pady=(0, 15))
        
        # Phone Number
        tk.Label(form_frame,
                text="Phone Number",
                font=('Segoe UI', 12),
                fg=self.colors['text'],
                bg=self.colors['white']).pack(anchor='w', pady=(0, 5))
                
        phone_var = tk.StringVar()
        ttk.Entry(form_frame,
                 textvariable=phone_var,
                 font=('Segoe UI', 12)).pack(fill='x', pady=(0, 15))
        
        # Date
        tk.Label(form_frame,
                text="Date",
                font=('Segoe UI', 12),
                fg=self.colors['text'],
                bg=self.colors['white']).pack(anchor='w', pady=(0, 5))
                
        date_var = tk.StringVar()
        date_entry = ttk.Entry(form_frame,
                              textvariable=date_var,
                              font=('Segoe UI', 12))
        date_entry.pack(fill='x', pady=(0, 15))
        date_entry.insert(0, "YYYY-MM-DD")  # Placeholder
        
        # Time
        tk.Label(form_frame,
                text="Time",
                font=('Segoe UI', 12),
                fg=self.colors['text'],
                bg=self.colors['white']).pack(anchor='w', pady=(0, 5))
                
        time_var = tk.StringVar()
        time_entry = ttk.Entry(form_frame,
                              textvariable=time_var,
                              font=('Segoe UI', 12))
        time_entry.pack(fill='x', pady=(0, 15))
        time_entry.insert(0, "HH:MM")  # Placeholder
        
        def schedule_tour():
            # Validate inputs
            client_name = client_name_var.get().strip()
            phone = phone_var.get().strip()
            date = date_var.get().strip()
            time = time_var.get().strip()
            
            if not all([client_name, phone, date, time]):
                messagebox.showerror("Error", "All fields are required")
                return
                
            # Create tour data
            tour_data = {
                'property_id': property_id,
                'client_name': client_name,
                'phone_number': phone,
                'date': date,
                'time': time
            }
            
            try:
                response = self.api_client.add_tour(tour_data)
                if response:
                    messagebox.showinfo("Success", "Tour scheduled successfully!")
                    dialog.destroy()
                    self.refresh_view()  # Changed from refresh_dashboard to refresh_view
                else:
                    messagebox.showerror("Error", "Failed to schedule tour")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
        
        # Buttons
        button_frame = tk.Frame(form_frame, bg=self.colors['white'])
        button_frame.pack(fill='x', pady=(20, 0))
        
        ttk.Button(button_frame,
                  text="Cancel",
                  style='Secondary.TButton',
                  command=dialog.destroy).pack(side='right', padx=(10, 0))
                  
        ttk.Button(button_frame,
                  text="Schedule Tour",
                  style='Primary.TButton',
                  command=schedule_tour).pack(side='right')

    def refresh_view(self):
        """Refresh the current view"""
        self.show_dashboard()