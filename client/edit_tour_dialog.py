import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import tkcalendar

class EditTourDialog:
    def __init__(self, parent, api_client, tour_id, refresh_callback):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Edit Tour")
        self.api_client = api_client
        self.tour_id = tour_id
        self.refresh_callback = refresh_callback
        
        # Define business hours (24-hour format)
        self.business_hours = {
            'start': 9,     # 9 AM
            'end': 17,      # 5 PM
            'lunch_start': 12,  # 12 PM
            'lunch_end': 13     # 1 PM
        }
        
        # Define working days (0 = Monday, 6 = Sunday)
        self.working_days = range(0, 5)  # Monday to Friday
        
        # Fetch tour data
        self.tour_data = self.api_client.get_tour(tour_id)
        if not self.tour_data:
            messagebox.showerror("Error", "Failed to fetch tour data")
            self.dialog.destroy()
            return
            
        self.setup_dialog()

    def validate_datetime(self, date, hour, minute, ampm):
        """Validate the complete datetime"""
        try:
            # Convert to 24-hour format
            hour_24 = hour
            if ampm == 'PM' and hour != 12:
                hour_24 += 12
            elif ampm == 'AM' and hour == 12:
                hour_24 = 0

            # Create datetime object
            new_time = datetime.combine(date, datetime.min.time().replace(hour=hour_24, minute=minute))
            current_time = datetime.now()

            # Check if date is in the future
            if new_time <= current_time:
                messagebox.showerror("Invalid Time", "Please select a future date and time.")
                return False

            # Check if it's a working day
            if new_time.weekday() not in self.working_days:
                messagebox.showerror("Invalid Day", "Tours can only be scheduled Monday through Friday.")
                return False

            # Check business hours
            if not (self.business_hours['start'] <= hour_24 < self.business_hours['end']):
                messagebox.showerror(
                    "Invalid Time", 
                    f"Please select a time between {self.business_hours['start']}:00 AM and {self.business_hours['end']-12}:00 PM."
                )
                return False

            # Check lunch hour
            if (self.business_hours['lunch_start'] <= hour_24 < self.business_hours['lunch_end']):
                messagebox.showerror(
                    "Invalid Time", 
                    "Tours cannot be scheduled during lunch hour (12:00 PM - 1:00 PM)."
                )
                return False

            return True
            
        except Exception as e:
            messagebox.showerror("Error", f"Invalid date/time: {str(e)}")
            return False

    def get_available_hours(self):
        """Returns a list of available hours in 12-hour format"""
        available_hours = []
        for hour in range(self.business_hours['start'], self.business_hours['end']):
            # Skip lunch hour
            if hour >= self.business_hours['lunch_start'] and hour < self.business_hours['lunch_end']:
                continue
            
            # Convert to 12-hour format
            if hour == 12:
                available_hours.append('12')
            elif hour > 12:
                available_hours.append(f'{hour-12:02d}')
            else:
                available_hours.append(f'{hour:02d}')
        
        return available_hours

    def save_changes(self):
        try:
            # Get the new date and time
            date = self.date_picker.get_date()
            hour = int(self.hour_var.get())
            minute = int(self.minute_var.get())
            ampm = self.ampm_var.get()

            # Validate inputs
            if not self.validate_datetime(date, hour, minute, ampm):
                return
            
            # Convert to 24-hour format
            if ampm == 'PM' and hour != 12:
                hour += 12
            elif ampm == 'AM' and hour == 12:
                hour = 0
                
            # Create new datetime
            new_time = datetime.combine(date, datetime.min.time().replace(hour=hour, minute=minute))
            
            # Update tour
            result = self.api_client.update_tour(self.tour_id, {'tour_time': new_time.isoformat()})
            if result:
                self.refresh_callback()
                self.dialog.destroy()
                messagebox.showinfo("Success", "Tour updated successfully")
            else:
                messagebox.showerror("Error", "Failed to update tour")
                
        except ValueError as e:
            messagebox.showerror("Error", "Please enter valid time values")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")