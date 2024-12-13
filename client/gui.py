import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
import tkcalendar
from .api_client import ApiClient

class ModernUI(ttk.Frame):
    def __init__(self, parent, state_manager):
        super().__init__(parent)
        self.parent = parent
        self.state_manager = state_manager
        
        # Initialize API client
        self.api_client = ApiClient()  # Uses default base_url
        
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
            'button_primary': '#8B1F2F',
            'button_primary_hover': '#A62639',
            'button_secondary': '#455A64',
            'button_secondary_hover': '#607D8B',
            'button_danger': '#C62828',
            'button_danger_hover': '#D32F2F',
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
        
        # Register as observer for state changes
        self.state_manager.add_observer(self.update_ui)

    def update_ui(self):
        """Update UI when state changes"""
        current_view = self.current_view
        if current_view:
            # Refresh the current view
            if current_view == 'dashboard':
                self.show_dashboard()
            elif current_view == 'tours':
                self.show_tours()
            elif current_view == 'properties':
                self.show_properties()
            elif current_view == 'reports':
                self.show_reports()
            elif current_view == 'settings':
                self.show_settings()

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

        # Add notebook (tab) styles
        self.style.configure(
            'Custom.TNotebook',
            background=self.colors['bg'],
            borderwidth=0,
            padding=5
        )
        
        # Configure the base tab style
        self.style.configure(
            'Custom.TNotebook.Tab',
            padding=(20, 10),
            background=self.colors['white'],
            foreground=self.colors['text'],  # Black text
            borderwidth=0,
            font=('Segoe UI', 10, 'bold')  # Made text bold for better visibility
        )
        
        # Updated tab styling for all states
        self.style.map('Custom.TNotebook.Tab',
            background=[
                ('selected', self.colors['button_primary']),  # Burgundy background when selected
                ('active', self.colors['button_primary_hover'])  # Slightly lighter burgundy on hover
            ],
            foreground=[
                ('selected', self.colors['text']),  # Black text
                ('active', self.colors['text'])     # Black text on hover
            ]
        )

        # Status label styles
        self.style.configure(
            'Status.TLabel',
            font=('Segoe UI', 9, 'bold'),
            padding=(8, 4),
            background=self.colors['white']
        )

        # Update Primary button style to ensure white text
        self.style.configure(
            'Primary.TButton',
            background=self.colors['button_primary'],
            foreground='white',  # Ensure white text
            font=('Segoe UI', 10),
            padding=(15, 8)
        )
        
        self.style.map('Primary.TButton',
            background=[
                ('active', self.colors['button_primary_hover']),
                ('pressed', self.colors['button_primary'])
            ],
            foreground=[
                ('active', 'white'),  # Keep text white on hover
                ('pressed', 'white')  # Keep text white when pressed
            ]
        )

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
        self.current_view = 'dashboard'
        self.clear_content()
        self.create_page_header("Dashboard", "Welcome to TourSync")
        
        # Main container
        container = ttk.Frame(self.content, style='Card.TFrame')
        container.pack(fill='both', expand=True, padx=30, pady=(0, 30))
        
        # Create tabs with custom style
        tab_control = ttk.Notebook(container, style='Custom.TNotebook')
        tab_control.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Active Tours Tab
        active_tab = ttk.Frame(tab_control, style='Card.TFrame')
        tab_control.add(active_tab, text='ACTIVE TOURS')
        
        # Inactive Tours Tab
        inactive_tab = ttk.Frame(tab_control, style='Card.TFrame')
        tab_control.add(inactive_tab, text='PAST TOURS')
        
        # Create tour list containers with proper styling
        self.active_tours_list = ttk.Frame(active_tab, style='Card.TFrame')
        self.active_tours_list.pack(fill='both', expand=True, padx=20, pady=20)
        
        self.inactive_tours_list = ttk.Frame(inactive_tab, style='Card.TFrame')
        self.inactive_tours_list.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Load tours
        self.load_tours()

    def show_tours(self):
        """Show tours view with management functionality"""
        self.current_view = 'tours'
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

    def create_tour_card(self, parent, tour, show_status=False):
        """Create a card displaying tour information"""
        card = ttk.Frame(parent, style='Card.TFrame')
        card.pack(fill='x', pady=(0, 10))
        
        # Tour info
        info_frame = ttk.Frame(card, style='Card.TFrame')
        info_frame.pack(fill='x', padx=15, pady=10)
        
        # Add status label for inactive tours with styled badge
        if show_status:
            status = tour.get('status', 'unknown').upper()
            status_colors = {
                'COMPLETED': {'fg': '#2D5A27', 'bg': '#E8F5E9'},  # Green
                'CANCELLED': {'fg': '#C62828', 'bg': '#FFEBEE'},  # Red
                'NO_SHOW': {'fg': '#F57C00', 'bg': '#FFF3E0'}    # Orange
            }
            
            status_frame = ttk.Frame(info_frame)
            status_frame.pack(anchor='w', pady=(0, 10))
            
            status_label = ttk.Label(
                status_frame,
                text=status,
                style='Status.TLabel'
            )
            status_label.pack(side='left')
            
            # Apply status-specific colors
            colors = status_colors.get(status, {'fg': self.colors['text'], 'bg': self.colors['border']})
            status_label.configure(foreground=colors['fg'], background=colors['bg'])
        
        # Property address with larger font
        ttk.Label(info_frame,
                 text=f"{tour.get('property_address', 'No address')}",
                 style='CardTitle.TLabel').pack(anchor='w', pady=(0, 5))
        
        # Tour details in a grid-like layout
        details_frame = ttk.Frame(info_frame, style='Card.TFrame')
        details_frame.pack(fill='x', pady=(5, 0))
        
        # Date and time
        date_time = f" {tour.get('date', 'No date')} at {tour.get('time', 'No time')}"
        ttk.Label(details_frame,
                 text=date_time,
                 style='CardBody.TLabel').pack(anchor='w')
        
        # Client info with icon
        client = f"👤 {tour.get('client_name', 'No name')}"
        ttk.Label(details_frame,
                 text=client,
                 style='CardBody.TLabel').pack(anchor='w', pady=(5, 0))
        
        # Only show action buttons for active tours
        if not show_status:
            separator = ttk.Frame(card, height=1, style='Separator.TFrame')
            separator.pack(fill='x', padx=15, pady=(5, 0))
            
            actions_frame = ttk.Frame(card, style='Card.TFrame')
            actions_frame.pack(fill='x', padx=15, pady=10)
            
            # Action buttons (using existing button styles)
            buttons = [
                ("Edit", 'Secondary.TButton', lambda t=tour: self.edit_tour(t)),
                ("Complete", 'Primary.TButton', lambda t=tour: self.complete_tour(t)),
                ("Cancel", 'Primary.TButton', lambda t=tour: self.cancel_tour(t)),
                ("No Show", 'Primary.TButton', lambda t=tour: self.mark_no_show(t))
            ]
            
            for text, style, command in buttons:
                btn = ttk.Button(actions_frame, text=text, style=style, command=command)
                btn.pack(side='left', padx=(0, 5))
            
            # Delete button on the right
            delete_btn = ttk.Button(
                actions_frame,
                text="Delete",
                style='Primary.TButton',
                command=lambda t=tour: self.delete_tour(t)
            )
            delete_btn.pack(side='right')

    def load_tours(self):
        """Load and display tours"""
        try:
            # Safely clear existing tours
            if hasattr(self, 'active_tours_list') and self.active_tours_list.winfo_exists():
                for widget in self.active_tours_list.winfo_children():
                    if widget.winfo_exists():
                        widget.destroy()
                        
            if hasattr(self, 'inactive_tours_list') and self.inactive_tours_list.winfo_exists():
                for widget in self.inactive_tours_list.winfo_children():
                    if widget.winfo_exists():
                        widget.destroy()
            
            # Get tours from API
            tours = self.api_client.get_tours()
            
            # Handle empty tours
            if not tours:
                if hasattr(self, 'active_tours_list') and self.active_tours_list.winfo_exists():
                    ttk.Label(self.active_tours_list,
                            text="No active tours",
                            style='Body.TLabel').pack(pady=20)
                if hasattr(self, 'inactive_tours_list') and self.inactive_tours_list.winfo_exists():
                    ttk.Label(self.inactive_tours_list,
                            text="No past tours",
                            style='Body.TLabel').pack(pady=20)
                return
            
            # Sort tours by date and time
            tours.sort(key=lambda x: (x.get('date', ''), x.get('time', '')))
            
            # Separate active and inactive tours
            active_tours = []
            inactive_tours = []
            
            for tour in tours:
                status = tour.get('status', '').lower()
                if status in ['completed', 'cancelled', 'no_show']:
                    inactive_tours.append(tour)
                else:
                    active_tours.append(tour)
            
            # Display active tours
            if hasattr(self, 'active_tours_list') and self.active_tours_list.winfo_exists():
                if active_tours:
                    for tour in active_tours:
                        self.create_tour_card(self.active_tours_list, tour)
                else:
                    ttk.Label(self.active_tours_list,
                            text="No active tours",
                            style='Body.TLabel').pack(pady=20)
            
            # Display inactive tours
            if hasattr(self, 'inactive_tours_list') and self.inactive_tours_list.winfo_exists():
                if inactive_tours:
                    for tour in inactive_tours:
                        self.create_tour_card(self.inactive_tours_list, tour, show_status=True)
                else:
                    ttk.Label(self.inactive_tours_list,
                            text="No past tours",
                            style='Body.TLabel').pack(pady=20)
                
        except Exception as e:
            print(f"Failed to load tours: {str(e)}")
            if hasattr(self, 'content') and self.content.winfo_exists():
                self.show_error_message(
                    "Unable to load tours",
                    "Please check your connection and try again."
                )

    def show_error_message(self, title, message):
        """Show error message with retry button
        
        Args:
            title (str): Error title
            message (str): Error message
        """
        error_frame = tk.Frame(self.content, bg=self.colors['white'])
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

    # Add other view methods (show_properties, show_reports, show_settings)
    def show_properties(self):
        """Show properties view"""
        self.current_view = 'properties'
        self.clear_content()
        self.create_page_header("Properties", "Manage your properties")
        
        # Main container
        container = ttk.Frame(self.content, style='Card.TFrame')
        container.pack(fill='both', expand=True, padx=30, pady=(0, 30))
        
        # Add property section
        add_section = ttk.Frame(container, style='Card.TFrame')
        add_section.pack(fill='x', padx=20, pady=(20, 10))
        
        # Property address entry
        address_frame = ttk.Frame(add_section)
        address_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(address_frame,
                 text="Property Address",
                 style='Body.TLabel').pack(side='left', padx=(0, 10))
        
        self.address_entry = ttk.Entry(address_frame, width=40)
        self.address_entry.pack(side='left', fill='x', expand=True)
        
        # Add button using create_styled_button
        add_btn = self.create_styled_button(
            add_section,
            "+ Add Property",
            'Primary.TButton',
            self.add_property
        )
        add_btn.pack(anchor='e', pady=(10, 0))
        
        # Separator
        ttk.Separator(container, orient='horizontal').pack(fill='x', padx=20, pady=20)
        
        # Properties list container
        self.properties_list = ttk.Frame(container, style='Card.TFrame')
        self.properties_list.pack(fill='both', expand=True, padx=20)
        
        # Load properties
        self.load_properties()

    def add_property(self):
        """Add a new property"""
        try:
            address = self.address_entry.get().strip()
            if not address:
                messagebox.showerror(
                    "Validation Error",
                    "Please enter a property address."
                )
                return
            
            property_data = {
                'address': address,
                'created_at': datetime.utcnow()
            }
            
            result = self.api_client.add_property(property_data)
            
            if result.get('success'):
                self.address_entry.delete(0, 'end')  # Clear the entry
                self.load_properties()  # Refresh the list
            else:
                messagebox.showerror(
                    "Error",
                    f"Failed to add property: {result.get('error', 'Unknown error')}"
                )
                
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Failed to add property: {str(e)}"
            )

    def load_properties(self):
        """Load and display properties"""
        try:
            # Clear existing properties
            if hasattr(self, 'properties_list') and self.properties_list.winfo_exists():
                for widget in self.properties_list.winfo_children():
                    if widget.winfo_exists():
                        widget.destroy()
            
            # Get properties from API
            properties = self.api_client.get_properties()
            
            if not properties:
                ttk.Label(self.properties_list,
                         text="No properties added yet",
                         style='Body.TLabel').pack(pady=20)
                return
            
            # Display properties
            for property_data in properties:
                self.create_property_card(self.properties_list, property_data)
                
        except Exception as e:
            print(f"Failed to load properties: {str(e)}")
            if hasattr(self, 'content') and self.content.winfo_exists():
                self.show_error_message(
                    "Unable to load properties",
                    "Please check your connection and try again."
                )

    def create_property_card(self, parent, property_data):
        """Create a clean property list item without borders"""
        # Main container
        card = ttk.Frame(parent, style='Card.TFrame')
        card.pack(fill='x', pady=1)  # Minimal spacing between items
        
        # Content container
        content = ttk.Frame(card, style='Card.TFrame')
        content.pack(fill='x', padx=10, pady=8)
        
        # Left side with house icon and address
        left_frame = ttk.Frame(content, style='Card.TFrame')
        left_frame.pack(side='left', fill='x', expand=True)
        
        # House icon and address in one line
        ttk.Label(left_frame,
                 text="🏠",
                 style='Body.TLabel').pack(side='left', padx=(0, 10))
                 
        ttk.Label(left_frame,
                 text=property_data.get('address', 'No address'),
                 style='Body.TLabel').pack(side='left')
        
        # Right side with action buttons
        actions_frame = ttk.Frame(content, style='Card.TFrame')
        actions_frame.pack(side='right')
        
        # Edit button with burgundy background and white text
        edit_btn = self.create_styled_button(
            actions_frame,
            "Edit",
            'Primary.TButton',
            lambda: self.edit_property(property_data)
        )
        edit_btn.pack(side='left', padx=(0, 5))
        
        # Delete button with burgundy background and white text
        delete_btn = self.create_styled_button(
            actions_frame,
            "Delete",
            'Primary.TButton',
            lambda: self.delete_property(property_data.get('_id'))
        )
        delete_btn.pack(side='left')
        
        # Simple hover effect
        def on_enter(e):
            card.configure(style='CardHover.TFrame')
            
        def on_leave(e):
            card.configure(style='Card.TFrame')
        
        card.bind('<Enter>', on_enter)
        card.bind('<Leave>', on_leave)

    def show_reports(self):
        """Show reports view"""
        self.current_view = 'reports'
        self.clear_content()
        self.create_page_header("Reports", "View your tour statistics")
        # Reports content here...

    def show_settings(self):
        """Show settings view"""
        self.current_view = 'settings'
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
        """Show tour editing form in the main content area"""
        self.clear_content()
        self.create_page_header("Edit Tour", "Update tour details")
        
        # Main container
        container = ttk.Frame(self.content, style='Card.TFrame')
        container.pack(fill='both', expand=True, padx=30, pady=(0, 30))
        
        # Form container
        form_frame = ttk.Frame(container, style='Card.TFrame')
        form_frame.pack(fill='x', padx=20, pady=20)
        
        # Pre-fill existing data
        self.property_var.set(tour.get('property_id', ''))
        self.client_name_var.set(tour.get('client_name', ''))
        self.phone_var.set(tour.get('phone_number', ''))
        
        # Property Selection
        property_dropdown = self.create_property_dropdown(form_frame)
        
        # Client Name
        ttk.Label(form_frame,
                 text="Client Name",
                 style='Body.TLabel').pack(anchor='w', pady=(15, 5))
        
        ttk.Entry(form_frame,
                 textvariable=self.client_name_var,
                 font=('Segoe UI', 11),
                 width=40).pack(fill='x')
        
        # Phone Number
        ttk.Label(form_frame,
                 text="Phone Number",
                 style='Body.TLabel').pack(anchor='w', pady=(15, 5))
        
        ttk.Entry(form_frame,
                 textvariable=self.phone_var,
                 font=('Segoe UI', 11),
                 width=40).pack(fill='x')
        
        # Tour Status
        ttk.Label(form_frame,
                 text="Tour Status",
                 style='Body.TLabel').pack(anchor='w', pady=(15, 5))
        
        status_frame = ttk.Frame(form_frame, style='Card.TFrame')
        status_frame.pack(fill='x', pady=(0, 15))
        
        def update_status(new_status):
            try:
                self.api_client.update_tour_status(tour['id'], new_status)
                self.load_tours()  # Refresh tours list
                self.show_tours()  # Return to tours view
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update status: {str(e)}")
        
        # Status buttons with consistent burgundy styling
        completed_btn = self.create_styled_button(
            status_frame,
            "✓ Completed",
            'Primary.TButton',
            lambda: update_status('completed')
        )
        completed_btn.pack(side='left', padx=(0, 5))
        
        cancelled_btn = self.create_styled_button(
            status_frame,
            "✗ Cancelled",
            'Primary.TButton',
            lambda: update_status('cancelled')
        )
        cancelled_btn.pack(side='left', padx=5)
        
        no_show_btn = self.create_styled_button(
            status_frame,
            "⚠ No Show",
            'Primary.TButton',
            lambda: update_status('no_show')
        )
        no_show_btn.pack(side='left', padx=5)
        
        # Buttons
        button_frame = ttk.Frame(form_frame, style='Card.TFrame')
        button_frame.pack(fill='x', pady=(15, 0))
        
        cancel_btn = self.create_styled_button(
            button_frame,
            "Cancel",
            'Primary.TButton',
            self.show_tours
        )
        cancel_btn.pack(side='left', padx=(0, 10))
        
        def save_changes():
            if not all([self.property_var.get(),
                       self.client_name_var.get(),
                       self.phone_var.get()]):
                messagebox.showerror("Error", "Please fill in all required fields")
                return
            
            updated_data = {
                'property_id': self.property_var.get(),
                'client_name': self.client_name_var.get(),
                'phone_number': self.phone_var.get()
            }
            
            try:
                self.api_client.update_tour(tour['id'], updated_data)
                self.show_tours()  # Return to tours list
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save changes: {str(e)}")
        
        save_btn = self.create_styled_button(
            button_frame,
            "Save Changes",
            'Primary.TButton',
            save_changes
        )
        save_btn.pack(side='right')

    def delete_tour(self, tour):
        """Delete a tour with confirmation"""
        if messagebox.askyesno("Confirm Delete", 
                              "Are you sure you want to delete this tour?"):
            try:
                # Get the tour ID (either 'id' or '_id')
                tour_id = tour.get('id') or tour.get('_id')
                if not tour_id:
                    raise ValueError("Invalid tour ID")
                    
                result = self.api_client.delete_tour(tour_id)
                if result['success']:
                    self.load_tours()  # Refresh the list
                else:
                    messagebox.showerror("Error", f"Failed to delete tour: {result.get('error', 'Unknown error')}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete tour: {str(e)}")

    def update_tour_status(self, tour, status, notes=None):
        """Update tour status"""
        try:
            result = self.api_client.update_tour_status(tour, status, notes)
            if result['success']:
                self.load_tours()  # Refresh the list
            else:
                messagebox.showerror("Error", f"Failed to update tour status: {result.get('error', 'Unknown error')}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update tour status: {str(e)}")

    def delete_property(self, property_id):
        """Delete a property with confirmation"""
        if messagebox.askyesno("Confirm Delete", 
                              "Are you sure you want to delete this property?"):
            try:
                result = self.api_client.delete_property(property_id)
                if result['success']:
                    self.load_properties()  # Refresh the list
                else:
                    messagebox.showerror("Error", 
                                       f"Failed to delete property: {result.get('error', 'Unknown error')}")
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

    def show_error_message(self, title, message):
        """Show error message with retry button
        
        Args:
            title (str): Error title
            message (str): Error message
        """
        error_frame = tk.Frame(self.content, bg=self.colors['white'])
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
        """Create a styled button with the specified style"""
        style_configs = {
            'Primary.TButton': {
                'bg': self.colors['button_primary'],
                'hover_bg': self.colors['button_primary_hover']
            },
            'Secondary.TButton': {
                'bg': self.colors['button_secondary'],
                'hover_bg': self.colors['button_secondary_hover']
            },
            'Danger.TButton': {
                'bg': self.colors['button_danger'],
                'hover_bg': self.colors['button_danger_hover']
            }
        }
        
        style_config = style_configs.get(style, style_configs['Primary.TButton'])
        
        button = tk.Button(parent,
                          text=text,
                          font=('Segoe UI', 11, 'bold'),
                          fg=self.colors['white'],
                          bg=style_config['bg'],
                          activebackground=style_config['hover_bg'],
                          activeforeground=self.colors['white'],
                          relief='flat',
                          cursor='hand2',
                          command=command)
        
        def on_enter(e):
            button['background'] = style_config['hover_bg']
            
        def on_leave(e):
            button['background'] = style_config['bg']
        
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