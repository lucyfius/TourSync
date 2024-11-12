import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import tkcalendar
from api_client import TourAPIClient

class ModernUI(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        
        # Initialize API client
        self.api_client = TourAPIClient()  # Uses default base_url
        # Or if you need a specific URL:
        # self.api_client = TourAPIClient("http://localhost:5000/api")
        
        # Modern color scheme with burgundy
        self.colors = {
            'bg': '#F5F5F5',           # Light gray background
            'sidebar': '#2C2C2C',       # Dark gray sidebar
            'sidebar_hover': '#3D3D3D', 
            'sidebar_active': '#8B1F2F', # Burgundy active state
            'white': '#FFFFFF',         # Pure white
            'text': '#1A1A1A',          # Near black for text
            'text_secondary': '#4A4A4A', # Medium gray for secondary text
            'text_light': '#E8E8E8',    # Light gray text for dark backgrounds
            'border': '#E0E0E0',        # Light gray borders
            'button_primary': '#8B1F2F',      # Burgundy for primary buttons
            'button_primary_hover': '#721A26', # Darker burgundy for hover
            'button_secondary': '#4A4A4A',    # Dark gray for secondary buttons
            'button_secondary_hover': '#3D3D3D', # Darker gray for hover
            'button_danger': '#8B1F2F',       # Changed to match burgundy
            'button_danger_hover': '#721A26',  # Changed to match burgundy hover
            'success': '#2D5A27',       # Dark green
            'error': '#D32F2F'          # Using same red as button_danger
        }
        
        # Initialize variables
        self.init_variables()
        
        # Setup UI components
        self.setup_styles()
        self.create_layout()
        
        # Show default view
        self.show_dashboard()

    def init_variables(self):
        """Initialize all necessary variables"""
        self.tours = []
        self.selected_tour = None
        self.property_var = tk.StringVar()
        self.client_name_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.time_var = tk.StringVar()
        self.current_view = None
        self.nav_buttons = []

    def setup_styles(self):
        """Setup sophisticated UI styles"""
        self.style = ttk.Style()
        
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
        
        self.style.configure('Body.TLabel',
                           background=self.colors['white'],
                           foreground=self.colors['text'],
                           font=('Segoe UI', 12))
                           
        # Primary button style (Burgundy fill)
        self.style.configure('Primary.TButton',
                            font=('Segoe UI', 11, 'bold'),
                            background=self.colors['button_primary'],
                            foreground=self.colors['white'],
                            padding=(20, 12),
                            relief='flat')
        
        self.style.map('Primary.TButton',
                       background=[('active', self.colors['button_primary_hover'])],
                       foreground=[('active', self.colors['white'])])
        
        # Secondary button style (Dark gray fill)
        self.style.configure('Secondary.TButton',
                            font=('Segoe UI', 11),
                            background=self.colors['button_secondary'],
                            foreground=self.colors['white'],
                            padding=(20, 12),
                            relief='flat')
        
        self.style.map('Secondary.TButton',
                       background=[('active', self.colors['button_secondary_hover'])],
                       foreground=[('active', self.colors['white'])])
        
        # Danger button style (now matching burgundy)
        self.style.configure('Danger.TButton',
                            font=('Segoe UI', 11),
                            background=self.colors['button_danger'],
                            foreground='white',
                            padding=(20, 12),
                            borderwidth=0,
                            relief='flat')

        self.style.map('Danger.TButton',
                       background=[('active', self.colors['button_danger_hover'])],
                       foreground=[('active', 'white')])

        # Apply rounded corners and shadow to all button styles
        for style in ['Primary.TButton', 'Secondary.TButton', 'Danger.TButton']:
            self.style.configure(style, borderradius=8)
            self.style.configure(style, borderwidth=1, relief='solid', bordercolor='#00000022')

    def create_layout(self):
        """Create main application layout"""
        # Main container
        self.main_container = tk.Frame(self, bg=self.colors['bg'])
        self.main_container.pack(fill='both', expand=True)
        
        # Create sidebar
        self.create_sidebar()
        
        # Create content area
        self.content = tk.Frame(self.main_container, bg=self.colors['bg'])
        self.content.pack(side='left', fill='both', expand=True)

    def create_sidebar(self):
        """Create modern sidebar"""
        self.sidebar = tk.Frame(self.main_container, bg=self.colors['sidebar'], width=280)
        self.sidebar.pack(side='left', fill='y')
        self.sidebar.pack_propagate(False)
        
        # App title
        title_frame = tk.Frame(self.sidebar, bg=self.colors['sidebar'])
        title_frame.pack(fill='x', pady=(30, 50), padx=25)
        
        tk.Label(title_frame,
                text="🏠",
                font=('Segoe UI', 24),
                fg=self.colors['button_primary'],
                bg=self.colors['sidebar']).pack(side='left', padx=(0, 10))
                
        tk.Label(title_frame,
                text="TourSync",
                font=('Segoe UI', 24, 'bold'),
                fg=self.colors['text_light'],
                bg=self.colors['sidebar']).pack(side='left')

        # Navigation items
        nav_items = [
            ('Dashboard', '📊', self.show_dashboard),
            ('Tours', '🗓️', self.show_tours),
            ('Properties', '🏘️', self.show_properties),
            ('Reports', '📈', self.show_reports),
            ('Settings', '⚙️', self.show_settings)
        ]
        
        for text, icon, command in nav_items:
            self.create_nav_item(text, icon, command)

    def create_nav_item(self, text, icon, command):
        """Create navigation item with modern styling"""
        btn = tk.Frame(self.sidebar, bg=self.colors['sidebar'], cursor='hand2')
        btn.pack(fill='x', pady=2)
        
        # Icon and text container
        content = tk.Frame(btn, bg=self.colors['sidebar'])
        content.pack(fill='x', padx=25, pady=12)
        
        # Icon
        tk.Label(content,
                text=icon,
                font=('Segoe UI', 16),
                fg=self.colors['text_light'],
                bg=self.colors['sidebar']).pack(side='left', padx=(0, 12))
        
        # Text
        tk.Label(content,
                text=text,
                font=('Segoe UI', 12),
                fg=self.colors['text_light'],
                bg=self.colors['sidebar']).pack(side='left')
        
        # Hover effects
        def on_enter(e):
            if btn not in self.nav_buttons or btn != self.current_view:
                btn.configure(bg=self.colors['sidebar_hover'])
                content.configure(bg=self.colors['sidebar_hover'])
                for widget in content.winfo_children():
                    widget.configure(bg=self.colors['sidebar_hover'])

        def on_leave(e):
            if btn not in self.nav_buttons or btn != self.current_view:
                btn.configure(bg=self.colors['sidebar'])
                content.configure(bg=self.colors['sidebar'])
                for widget in content.winfo_children():
                    widget.configure(bg=self.colors['sidebar'])

        def on_click(e):
            self.set_active_nav(btn)
            command()

        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
        btn.bind('<Button-1>', on_click)
        for widget in content.winfo_children():
            widget.bind('<Button-1>', on_click)
            widget.bind('<Enter>', on_enter)
            widget.bind('<Leave>', on_leave)

        self.nav_buttons.append(btn)

    def set_active_nav(self, active_btn):
        """Set active navigation item"""
        for btn in self.nav_buttons:
            if btn == active_btn:
                btn.configure(bg=self.colors['sidebar_active'])
                for widget in btn.winfo_children():
                    widget.configure(bg=self.colors['sidebar_active'])
                    for w in widget.winfo_children():
                        w.configure(bg=self.colors['sidebar_active'])
            else:
                btn.configure(bg=self.colors['sidebar'])
                for widget in btn.winfo_children():
                    widget.configure(bg=self.colors['sidebar'])
                    for w in widget.winfo_children():
                        w.configure(bg=self.colors['sidebar'])
        
        self.current_view = active_btn

    def clear_content(self):
        """Clear content area"""
        for widget in self.content.winfo_children():
            widget.destroy()

    def create_page_header(self, title, description=None):
        """Create consistent page header"""
        header_frame = ttk.Frame(self.content, style='Card.TFrame')
        header_frame.pack(fill='x', padx=30, pady=30)
        
        ttk.Label(header_frame,
                 text=title,
                 style='Header.TLabel').pack(anchor='w')
        
        if description:
            ttk.Label(header_frame,
                     text=description,
                     style='Body.TLabel').pack(anchor='w', pady=(10, 0))

    def show_dashboard(self):
        """Show dashboard view"""
        self.clear_content()
        self.create_page_header("Dashboard", "Welcome to TourSync")
        
        # Main container
        container = ttk.Frame(self.content, style='Card.TFrame')
        container.pack(fill='both', expand=True, padx=30, pady=(0, 30))
        
        # Upcoming Tours Section
        tours_frame = ttk.Frame(container, style='Card.TFrame')
        tours_frame.pack(fill='x', padx=20, pady=20)
        
        ttk.Label(tours_frame,
                 text="Upcoming Tours",
                 style='SubHeader.TLabel').pack(anchor='w', pady=(0, 15))
        
        try:
            # Get tours from API
            tours = self.api_client.get_tours()
            
            if not tours:
                ttk.Label(tours_frame,
                         text="No upcoming tours scheduled",
                         style='Body.TLabel').pack(pady=10)
                return
            
            # Sort tours by date and time
            tours.sort(key=lambda x: (x['date'], x['time']))
            
            # Display tours
            for tour in tours:
                self.create_tour_card(tours_frame, tour)
                
        except Exception as e:
            print(f"Failed to load tours: {str(e)}")
            self.show_error_message("Unable to load tours", 
                                  "Please check your connection and try again.")

    def show_tours(self):
        """Show tours view with management functionality"""
        self.clear_content()
        self.create_page_header("Tours", "Manage your property tours")
        
        # Main container
        container = ttk.Frame(self.content, style='Card.TFrame')
        container.pack(fill='both', expand=True, padx=30, pady=(0, 30))
        
        # Add tour button with new styling
        btn_frame = ttk.Frame(container, style='Card.TFrame')
        btn_frame.pack(fill='x', padx=20, pady=20)
        
        schedule_btn = self.create_styled_button(
            btn_frame,
            "+ Schedule New Tour",
            'Primary.TButton',
            self.show_add_tour
        )
        schedule_btn.pack(side='left')
        
        # Tours list
        self.tours_list = ttk.Frame(container, style='Card.TFrame')
        self.tours_list.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        self.load_tours()

    def create_tour_card(self, parent, tour):
        """Create individual tour card with status indicator"""
        card = tk.Frame(parent, bg=self.colors['white'], relief='solid', borderwidth=1)
        card.pack(fill='x', pady=8, padx=2)
        
        # Status indicator
        status = tour.get('status', 'scheduled')
        status_colors = {
            'scheduled': '#8B1F2F',  # Burgundy
            'completed': '#81C784',  # Green
            'cancelled': '#E57373',  # Red
            'no_show': '#9575CD'    # Purple
        }
        
        status_bar = tk.Frame(card,
                             bg=status_colors.get(status, self.colors['button_primary']),
                             height=4)
        status_bar.pack(fill='x')
        
        content = tk.Frame(card, bg=self.colors['white'])
        content.pack(fill='x', padx=20, pady=15)
        
        # Convert time to 12-hour format
        try:
            time_24 = datetime.strptime(tour.get('time', '00:00'), '%H:%M')
            time_12 = time_24.strftime('%I:%M %p')
        except ValueError:
            time_12 = tour.get('time', 'N/A')
        
        # Tour info with 12-hour time
        tk.Label(content,
                text=f"📅 {tour.get('date', 'N/A')} at {time_12}",
                font=('Segoe UI', 14, 'bold'),
                fg=self.colors['text'],
                bg=self.colors['white']).pack(anchor='w')
        
        tk.Label(content,
                text=f"🏠 {tour.get('property_address', tour.get('property_id', 'N/A'))}",
                font=('Segoe UI', 12),
                fg=self.colors['text_secondary'],
                bg=self.colors['white']).pack(anchor='w', pady=(10, 0))
        
        tk.Label(content,
                text=f"👤 {tour.get('client_name', 'N/A')}",
                font=('Segoe UI', 12),
                fg=self.colors['text_secondary'],
                bg=self.colors['white']).pack(anchor='w', pady=(5, 0))
        
        tk.Label(content,
                text=f"📱 {tour.get('phone_number', 'N/A')}",
                font=('Segoe UI', 12),
                fg=self.colors['text_secondary'],
                bg=self.colors['white']).pack(anchor='w', pady=(5, 0))
        
        # Actions
        actions = tk.Frame(content, bg=self.colors['white'])
        actions.pack(anchor='w', pady=(15, 0))
        
        edit_btn = self.create_styled_button(
            actions, 
            "Edit", 
            'Secondary.TButton',
            lambda: self.edit_tour(tour)
        )
        edit_btn.pack(side='left', padx=(0, 10))
        
        delete_btn = self.create_styled_button(
            actions, 
            "Delete", 
            'Danger.TButton',
            lambda: self.delete_tour(tour)
        )
        delete_btn.pack(side='left')

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
                         style='Body.TLabel').pack(pady=20)
                return
            
            # Sort tours by date and time
            tours.sort(key=lambda x: (x['date'], x['time']))
            
            # Display tours
            for tour in tours:
                self.create_tour_card(self.tours_list, tour)
                
        except Exception as e:
            print(f"Failed to load tours: {str(e)}")
            self.show_error_message("Unable to load tours", 
                                  "Please check your connection and try again.")

    def show_error_message(self, title, message):
        """Show error message with modern styling"""
        error_frame = tk.Frame(self.tours_list, bg=self.colors['white'])
        error_frame.pack(fill='x', pady=20)
        
        tk.Label(error_frame,
                text=f"⚠️ {title}",
                font=('Segoe UI', 12, 'bold'),
                fg=self.colors['error'],
                bg=self.colors['white']).pack(anchor='w')
                
        tk.Label(error_frame,
                text=message,
                font=('Segoe UI', 12),
                fg=self.colors['text_secondary'],
                bg=self.colors['white']).pack(anchor='w', pady=(5, 10))
                
        ttk.Button(error_frame,
                  text="Try Again",
                  style='Primary.TButton',
                  command=self.load_tours).pack(anchor='w')

    # Add other view methods (show_properties, show_reports, show_settings)
    def show_properties(self):
        """Show properties view with management functionality"""
        self.clear_content()
        self.create_page_header("Properties", "Manage your properties")
        
        # Main container
        container = ttk.Frame(self.content, style='Card.TFrame')
        container.pack(fill='both', expand=True, padx=30, pady=(0, 30))
        
        # Add property button
        btn_frame = ttk.Frame(container, style='Card.TFrame')
        btn_frame.pack(fill='x', padx=20, pady=20)
        
        add_property_btn = self.create_styled_button(
            btn_frame,
            "+ Add Property",
            'Primary.TButton',
            self.show_add_property_form
        )
        add_property_btn.pack(side='left')
        
        # Properties list
        self.properties_list = ttk.Frame(container, style='Card.TFrame')
        self.properties_list.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        self.load_properties()

    def show_add_property_form(self):
        """Show property form integrated in the main window"""
        self.clear_content()
        self.create_page_header("Add Property", "Enter new property details")
        
        # Main container
        container = ttk.Frame(self.content, style='Card.TFrame')
        container.pack(fill='both', expand=True, padx=30, pady=(0, 30))
        
        # Form container
        form_frame = ttk.Frame(container, style='Card.TFrame')
        form_frame.pack(fill='x', padx=20, pady=20)
        
        # Address field
        ttk.Label(form_frame,
                 text="Property Address",
                 style='Body.TLabel').pack(anchor='w', pady=(0, 5))
        
        address_var = tk.StringVar()
        address_entry = ttk.Entry(form_frame,
                                textvariable=address_var,
                                font=('Segoe UI', 11),
                                width=40)
        address_entry.pack(fill='x')
        
        # Buttons
        button_frame = ttk.Frame(form_frame, style='Card.TFrame')
        button_frame.pack(fill='x', pady=(20, 0))
        
        def save_property():
            address = address_var.get().strip()
            if not address:
                messagebox.showerror("Error", "Please enter a property address")
                return
                
            try:
                self.api_client.add_property({'address': address})
                self.show_properties()  # Return to properties list
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add property: {str(e)}")
        
        # Cancel button (burgundy filled)
        cancel_btn = tk.Button(button_frame,
                              text="Cancel",
                              font=('Segoe UI', 11, 'bold'),
                              fg=self.colors['white'],
                              bg=self.colors['button_primary'],
                              activebackground=self.colors['button_primary_hover'],
                              activeforeground=self.colors['white'],
                              relief='flat',
                              cursor='hand2',
                              command=self.show_properties)
        cancel_btn.pack(side='left', padx=(0, 10))
        
        # Save button (burgundy filled)
        save_btn = tk.Button(button_frame,
                            text="Save Property",
                            font=('Segoe UI', 11, 'bold'),
                            fg=self.colors['white'],
                            bg=self.colors['button_primary'],
                            activebackground=self.colors['button_primary_hover'],
                            activeforeground=self.colors['white'],
                            relief='flat',
                            cursor='hand2',
                            command=save_property)
        save_btn.pack(side='right')

    def load_properties(self):
        """Load and display properties"""
        try:
            # Clear existing properties
            for widget in self.properties_list.winfo_children():
                widget.destroy()
            
            properties = self.api_client.get_properties()
            
            if not properties:
                ttk.Label(self.properties_list,
                         text="No properties added",
                         style='Body.TLabel').pack(pady=20)
                return
            
            # Display properties
            for prop in properties:
                self.create_property_card(prop)
                
        except Exception as e:
            print(f"Failed to load properties: {str(e)}")
            self.show_error_message("Unable to load properties", 
                                  "Please check your connection and try again.")

    def create_property_card(self, property_data):
        """Create individual property card"""
        card = tk.Frame(self.properties_list, bg=self.colors['white'], relief='solid', borderwidth=1)
        card.pack(fill='x', pady=8, padx=2)
        
        content = tk.Frame(card, bg=self.colors['white'])
        content.pack(fill='x', padx=20, pady=15)
        
        # Property address
        tk.Label(content,
                text=f"🏠 {property_data['address']}",
                font=('Segoe UI', 14, 'bold'),
                fg=self.colors['text'],
                bg=self.colors['white']).pack(anchor='w')
        
        # Actions
        actions = tk.Frame(content, bg=self.colors['white'])
        actions.pack(anchor='w', pady=(15, 0))
        
        edit_btn = self.create_styled_button(
            actions,
            "Edit",
            'Secondary.TButton',
            lambda: self.edit_property(property_data)
        )
        edit_btn.pack(side='left', padx=(0, 10))
        
        delete_btn = self.create_styled_button(
            actions,
            "Delete",
            'Danger.TButton',
            lambda: self.delete_property(property_data['id'])
        )
        delete_btn.pack(side='left')

    def show_reports(self):
        self.clear_content()
        self.create_page_header("Reports", "View your tour statistics")
        # Reports content here...

    def show_settings(self):
        self.clear_content()
        self.create_page_header("Settings", "Configure your preferences")
        # Settings content here...

    def create_property_dropdown(self, parent):
        """Create property dropdown with modern styling"""
        properties_frame = ttk.Frame(parent, style='Card.TFrame')
        properties_frame.pack(fill='x', pady=(0, 15))
        
        ttk.Label(properties_frame,
                 text="Select Property",
                 style='Body.TLabel').pack(anchor='w', pady=(0, 5))
        
        # Get properties from API
        try:
            properties = self.api_client.get_properties()
            property_addresses = [prop['address'] for prop in properties]
        except Exception as e:
            property_addresses = []
            print(f"Error loading properties: {str(e)}")
        
        # Create Combobox with custom styling
        self.property_var.set('')  # Clear previous selection
        property_dropdown = ttk.Combobox(properties_frame,
                                       textvariable=self.property_var,
                                       values=property_addresses,
                                       state='readonly',
                                       font=('Segoe UI', 11),
                                       width=40)
        property_dropdown.pack(fill='x')
        
        return property_dropdown

    def show_add_tour(self):
        """Show tour scheduling form in the main content area"""
        self.clear_content()
        self.create_page_header("Schedule New Tour", "Add a new property tour")
        
        # Main container
        container = ttk.Frame(self.content, style='Card.TFrame')
        container.pack(fill='both', expand=True, padx=30, pady=(0, 30))
        
        # Form container with white background
        form_frame = ttk.Frame(container, style='Card.TFrame')
        form_frame.pack(fill='x', padx=20, pady=20)
        
        # Property Selection
        ttk.Label(form_frame,
                 text="Select Property",
                 style='Body.TLabel').pack(anchor='w', pady=(0, 5))
        
        properties = self.get_property_list()
        property_dropdown = ttk.Combobox(form_frame,
                                       textvariable=self.property_var,
                                       values=properties,
                                       state='readonly',
                                       font=('Segoe UI', 11),
                                       width=40)
        property_dropdown.pack(fill='x', pady=(0, 15))
        
        # Client Name
        ttk.Label(form_frame,
                 text="Client Name",
                 style='Body.TLabel').pack(anchor='w', pady=(0, 5))
        
        ttk.Entry(form_frame,
                 textvariable=self.client_name_var,
                 font=('Segoe UI', 11),
                 width=40).pack(fill='x', pady=(0, 15))
        
        # Phone Number
        ttk.Label(form_frame,
                 text="Phone Number",
                 style='Body.TLabel').pack(anchor='w', pady=(0, 5))
        
        ttk.Entry(form_frame,
                 textvariable=self.phone_var,
                 font=('Segoe UI', 11),
                 width=40).pack(fill='x', pady=(0, 15))
        
        # Tour Date
        ttk.Label(form_frame,
                 text="Tour Date (MM/DD/YYYY)",
                 style='Body.TLabel').pack(anchor='w', pady=(0, 5))
        
        date_var = tk.StringVar()
        date_entry = ttk.Entry(form_frame,
                              textvariable=date_var,
                              font=('Segoe UI', 11),
                              width=40)
        date_entry.pack(fill='x', pady=(0, 15))
        
        # Tour Time
        ttk.Label(form_frame,
                 text="Tour Time (HH:MM AM/PM)",
                 style='Body.TLabel').pack(anchor='w', pady=(0, 5))
        
        time_var = tk.StringVar()
        time_entry = ttk.Entry(form_frame,
                              textvariable=time_var,
                              font=('Segoe UI', 11),
                              width=40)
        time_entry.pack(fill='x', pady=(0, 15))
        
        # Buttons
        button_frame = ttk.Frame(form_frame, style='Card.TFrame')
        button_frame.pack(fill='x', pady=(15, 0))
        
        # Cancel button
        cancel_btn = self.create_styled_button(
            button_frame,
            "Cancel",
            'Secondary.TButton',
            self.show_tours
        )
        cancel_btn.pack(side='left', padx=(0, 10))
        
        def save_tour():
            try:
                # Parse and validate date
                tour_date = datetime.strptime(date_var.get(), '%m/%d/%Y').date()
                
                # Parse and validate time
                try:
                    time_obj = datetime.strptime(time_var.get(), '%I:%M %p')
                    hour = time_obj.hour
                    minute = time_obj.minute
                except ValueError:
                    messagebox.showerror("Error", "Please enter time in format HH:MM AM/PM (e.g., 03:20 PM)")
                    return
                
                # Create tour data
                tour_data = {
                    'property_id': self.property_var.get(),
                    'client_name': self.client_name_var.get(),
                    'phone_number': self.phone_var.get(),
                    'date': tour_date.strftime('%Y-%m-%d'),
                    'time': f"{hour:02d}:{minute:02d}",
                    'duration': 60  # Fixed 1-hour duration
                }
                
                if not all([tour_data['property_id'],
                           tour_data['client_name'],
                           tour_data['phone_number']]):
                    messagebox.showerror("Error", "Please fill in all required fields")
                    return
                    
                self.api_client.add_tour(tour_data)
                self.show_tours()
                
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid date in MM/DD/YYYY format")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save tour: {str(e)}")
        
        # Schedule button
        schedule_btn = self.create_styled_button(
            button_frame,
            "Schedule Tour",
            'Primary.TButton',
            save_tour
        )
        schedule_btn.pack(side='right')

    def edit_tour(self, tour):
        """Show dialog to edit an existing tour"""
        dialog = tk.Toplevel(self)
        dialog.title("Edit Tour")
        dialog.geometry("500x700")
        dialog.configure(bg=self.colors['white'])
        
        # Make dialog modal
        dialog.transient(self)
        dialog.grab_set()
        
        # Header
        header_frame = ttk.Frame(dialog, style='Card.TFrame')
        header_frame.pack(fill='x', padx=20, pady=20)
        
        ttk.Label(header_frame,
                 text="Edit Tour",
                 style='SubHeader.TLabel').pack(anchor='w')
        
        # Form container
        form_frame = ttk.Frame(dialog, style='Card.TFrame')
        form_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Pre-fill existing data
        self.property_var.set(tour.get('property_id', ''))
        self.client_name_var.set(tour.get('client_name', ''))
        self.phone_var.set(tour.get('phone_number', ''))
        
        # Add form fields (similar to add_tour)
        property_dropdown = self.create_property_dropdown(form_frame)
        
        # ... (Add other fields similar to add_tour dialog) ...
        
        # Tour Status
        ttk.Label(form_frame,
                 text="Tour Status",
                 style='Body.TLabel').pack(anchor='w', pady=(15, 5))
        
        status_var = tk.StringVar(value=tour.get('status', 'scheduled'))
        status_frame = ttk.Frame(form_frame)
        status_frame.pack(fill='x', pady=(0, 15))
        
        def update_status(new_status):
            try:
                self.api_client.update_tour_status(tour['id'], new_status)
                status_var.set(new_status)
                self.load_tours()  # Refresh tours list
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update status: {str(e)}")
        
        # Status buttons
        ttk.Button(status_frame,
                  text="✓ Completed",
                  style='Primary.TButton',
                  command=lambda: update_status('completed')).pack(side='left', padx=(0, 5))
        
        ttk.Button(status_frame,
                  text="✗ Cancelled",
                  style='Danger.TButton',
                  command=lambda: update_status('cancelled')).pack(side='left', padx=5)
        
        ttk.Button(status_frame,
                  text="⚠ No Show",
                  style='Secondary.TButton',
                  command=lambda: update_status('no_show')).pack(side='left', padx=5)
        
        # Save/Cancel buttons
        button_frame = ttk.Frame(dialog, style='Card.TFrame')
        button_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        ttk.Button(button_frame,
                  text="Cancel",
                  style='Secondary.TButton',
                  command=dialog.destroy).pack(side='left', padx=(0, 10))
        
        def save_changes():
            # Validate and save changes
            if not all([self.property_var.get(),
                       self.client_name_var.get(),
                       self.phone_var.get()]):
                messagebox.showerror("Error", "Please fill in all required fields")
                return
            
            # Update tour data
            updated_data = {
                'property_id': self.property_var.get(),
                'client_name': self.client_name_var.get(),
                'phone_number': self.phone_var.get(),
                'status': status_var.get(),
                # Add other fields...
            }
            
            try:
                self.api_client.update_tour(tour['id'], updated_data)
                dialog.destroy()
                self.load_tours()  # Refresh tours list
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save changes: {str(e)}")
        
        ttk.Button(button_frame,
                  text="Save Changes",
                  style='Primary.TButton',
                  command=save_changes).pack(side='right')

    def delete_tour(self, tour):
        """Delete a tour with confirmation"""
        if messagebox.askyesno("Confirm Delete", 
                              "Are you sure you want to delete this tour?"):
            try:
                if self.api_client.delete_tour(tour['id']):
                    self.load_tours()  # Refresh the list
                else:
                    messagebox.showerror("Error", "Failed to delete tour")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete tour: {str(e)}")

    def delete_property(self, property_id):
        """Delete a property with confirmation"""
        if messagebox.askyesno("Confirm Delete", 
                              "Are you sure you want to delete this property? This cannot be undone."):
            try:
                if self.api_client.delete_property(property_id):
                    self.load_properties()  # Refresh the properties list
                else:
                    messagebox.showerror("Error", 
                                       "Failed to delete property. It may have associated tours.")
            except Exception as e:
                messagebox.showerror("Error", 
                                   f"Failed to delete property: {str(e)}")

    def show_loading(self, parent, message="Loading..."):
        """Show loading indicator"""
        loading_frame = tk.Frame(parent, bg=self.colors['white'])
        loading_frame.pack(fill='both', expand=True)
        
        tk.Label(loading_frame,
                text="⌛",
                font=('Segoe UI', 24),
                fg=self.colors['primary'],
                bg=self.colors['white']).pack(pady=(20, 10))
                
        tk.Label(loading_frame,
                text=message,
                font=('Segoe UI', 12),
                fg=self.colors['text_secondary'],
                bg=self.colors['white']).pack()
        
        return loading_frame

    def show_error_message(self, parent, title, message):
        """Show error message with retry button"""
        error_frame = tk.Frame(parent, bg=self.colors['white'])
        error_frame.pack(fill='x', pady=20)
        
        tk.Label(error_frame,
                text=f"⚠️ {title}",
                font=('Segoe UI', 12, 'bold'),
                fg=self.colors['error'],
                bg=self.colors['white']).pack(anchor='w')
                
        tk.Label(error_frame,
                text=message,
                font=('Segoe UI', 12),
                fg=self.colors['text_secondary'],
                bg=self.colors['white']).pack(anchor='w', pady=(5, 10))
        
        return error_frame

    def create_styled_button(self, parent, text, style, command):
        """Create a styled button with consistent burgundy appearance"""
        button = tk.Button(parent,
                          text=text,
                          font=('Segoe UI', 11, 'bold'),
                          fg=self.colors['white'],
                          bg=self.colors['button_primary'],
                          activebackground=self.colors['button_primary_hover'],
                          activeforeground=self.colors['white'],
                          relief='flat',
                          cursor='hand2',
                          command=command)
        
        def on_enter(e):
            button['background'] = self.colors['button_primary_hover']
            
        def on_leave(e):
            button['background'] = self.colors['button_primary']
        
        button.bind('<Enter>', on_enter)
        button.bind('<Leave>', on_leave)
        
        return button

    def get_property_list(self):
        """Get list of properties from API"""
        try:
            properties = self.api_client.get_properties()
            return [prop['address'] for prop in properties] if properties else []
        except Exception as e:
            print(f"Error loading properties: {str(e)}")
            return []

    def edit_property(self, property_data):
        """Show property editing form in the main window"""
        self.clear_content()
        self.create_page_header("Edit Property", "Update property details")
        
        # Main container
        container = ttk.Frame(self.content, style='Card.TFrame')
        container.pack(fill='both', expand=True, padx=30, pady=(0, 30))
        
        # Form container
        form_frame = ttk.Frame(container, style='Card.TFrame')
        form_frame.pack(fill='x', padx=20, pady=20)
        
        # Address field
        ttk.Label(form_frame,
                 text="Property Address",
                 style='Body.TLabel').pack(anchor='w', pady=(0, 5))
        
        address_var = tk.StringVar(value=property_data['address'])
        address_entry = ttk.Entry(form_frame,
                                textvariable=address_var,
                                font=('Segoe UI', 11),
                                width=40)
        address_entry.pack(fill='x')
        
        # Buttons
        button_frame = ttk.Frame(form_frame, style='Card.TFrame')
        button_frame.pack(fill='x', pady=(20, 0))
        
        def save_changes():
            address = address_var.get().strip()
            if not address:
                messagebox.showerror("Error", "Please enter a property address")
                return
                
            try:
                self.api_client.update_property(property_data['id'], {'address': address})
                self.show_properties()  # Return to properties list
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update property: {str(e)}")
        
        # Cancel button (burgundy filled)
        cancel_btn = self.create_styled_button(
            button_frame,
            "Cancel",
            'Primary.TButton',
            self.show_properties
        )
        cancel_btn.pack(side='left', padx=(0, 10))
        
        # Save button (burgundy filled)
        save_btn = self.create_styled_button(
            button_frame,
            "Save Changes",
            'Primary.TButton',
            save_changes
        )
        save_btn.pack(side='right')