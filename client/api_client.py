import requests
from datetime import datetime
from config import API_BASE_URL

class APIError(Exception):
    def __init__(self, message, status_code=None):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class TourAPIClient:
    def __init__(self):
        self.base_url = API_BASE_URL
        self.session = requests.Session()
    
    def _handle_request_error(self, error, action):
        """Standardized error handling for API requests"""
        if isinstance(error, requests.RequestException):
            if error.response is not None:
                status_code = error.response.status_code
                try:
                    error_message = error.response.json().get('error', str(error))
                except ValueError:
                    error_message = str(error)
                raise APIError(f"Error {action}: {error_message}", status_code)
            raise APIError(f"Network error while {action}: {str(error)}")
        raise APIError(f"Unexpected error while {action}: {str(error)}")

    def create_tour(self, property_id, tour_time, client_name, phone_number):
        """Create a new tour"""
        try:
            data = {
                "property_id": property_id,
                "tour_time": tour_time.isoformat(),
                "client_name": client_name,
                "phone_number": phone_number
            }
            response = self.session.post(f"{self.base_url}/tours", json=data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self._handle_request_error(e, "creating tour")

    def get_tours(self):
        """Get all tours"""
        try:
            response = requests.get(f"{self.base_url}/tours")
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error fetching tours: {response.text}")
                return []
        except Exception as e:
            print(f"Error fetching tours: {str(e)}")
            return []

    def delete_tour(self, tour_id):
        """Delete a tour"""
        try:
            response = requests.delete(f"{self.base_url}/tours/{tour_id}")
            if response.status_code == 200:
                return True
            else:
                print(f"Error deleting tour: {response.text}")
                return False
        except Exception as e:
            print(f"Error deleting tour: {str(e)}")
            return False

    def update_tour(self, tour_id, tour_data):
        """Update an existing tour"""
        try:
            response = self.session.put(f"{self.base_url}/tours/{tour_id}", json=tour_data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error updating tour: {str(e)}")
            return None

    def get_properties(self):
        """Get all properties"""
        try:
            response = requests.get(f"{self.base_url}/properties")
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error fetching properties: {response.text}")
                return []
        except Exception as e:
            print(f"Error fetching properties: {str(e)}")
            return []

    def add_property(self, property_data):
        """Add a new property"""
        try:
            response = requests.post(f"{self.base_url}/properties", json=property_data)
            if response.status_code == 201:
                return response.json()
            else:
                print(f"Error adding property: {response.text}")
                return None
        except Exception as e:
            print(f"Error adding property: {str(e)}")
            return None

    def delete_property(self, property_id):
        """Delete a property"""
        try:
            response = requests.delete(f"{self.base_url}/properties/{property_id}")
            if response.status_code == 200:
                return True
            else:
                print(f"Error deleting property: {response.text}")
                return False
        except Exception as e:
            print(f"Error deleting property: {str(e)}")
            return False

    def update_property(self, property_id, property_data):
        """Update an existing property"""
        try:
            response = requests.put(f"{self.base_url}/properties/{property_id}", json=property_data)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error updating property: {response.text}")
                return None
        except Exception as e:
            print(f"Error updating property: {str(e)}")
            return None

    def add_tour(self, tour_data):
        """Add a new tour"""
        try:
            # Debug print
            print("Client sending tour data:", tour_data)
            
            response = requests.post(f"{self.base_url}/tours", json=tour_data)
            
            # Debug print
            print("Server response:", response.text)
            
            if response.status_code == 201:
                return response.json()
            else:
                print(f"Error adding tour: {response.text}")
                return None
        except Exception as e:
            print(f"Error adding tour: {str(e)}")
            return None
