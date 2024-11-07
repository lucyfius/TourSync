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
        self.cache = {}
        self.cache_timeout = 300  # 5 minutes

    def _handle_request_error(self, e, operation):
        """Centralized error handling"""
        if isinstance(e, requests.exceptions.RequestException):
            if hasattr(e.response, 'status_code'):
                status_code = e.response.status_code
                try:
                    error_msg = e.response.json().get('error', str(e))
                except:
                    error_msg = str(e)
            else:
                status_code = 500
                error_msg = str(e)
        else:
            status_code = 500
            error_msg = str(e)

        print(f"Error during {operation}: {error_msg}")
        raise APIError(error_msg, status_code)

    def get_tours(self):
        """Fetch all tours with caching"""
        try:
            response = self.session.get(f"{self.base_url}/tours")
            response.raise_for_status()
            tours = response.json()
            return tours
        except Exception as e:
            self._handle_request_error(e, "fetching tours")

    def create_tour(self, property_id, tour_time, client_name, phone_number):
        """Create a new tour"""
        try:
            data = {
                "property_id": property_id,
                "tour_time": tour_time.isoformat(),
                "client_name": client_name,
                "phone_number": phone_number
            }
            response = requests.post(f"{self.base_url}/tours", json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error creating tour: {e}")
            return None

    def get_tour(self, tour_id):
        """Fetch a specific tour by ID"""
        try:
            response = self.session.get(f"{self.base_url}/tours/{tour_id}")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching tour: {e}")
            return None

    def update_tour(self, tour_id, data):
        """Update a tour"""
        try:
            response = self.session.put(f"{self.base_url}/tours/{tour_id}", json=data)
            response.raise_for_status()
            self.cache.pop('tours', None)  # Invalidate cache
            return response.json()
        except requests.RequestException as e:
            print(f"Error updating tour: {e}")
            return None

    def cancel_tour(self, tour_id):
        """Cancel a tour"""
        try:
            response = self.session.post(f"{self.base_url}/tours/{tour_id}/cancel")
            response.raise_for_status()
            self.cache.pop('tours', None)  # Invalidate cache
            return response.json()
        except requests.RequestException as e:
            print(f"Error cancelling tour: {e}")
            return None

    def complete_tour(self, tour_id):
        """Complete a tour"""
        try:
            response = self.session.post(f"{self.base_url}/tours/{tour_id}/complete")
            response.raise_for_status()
            self.cache.pop('tours', None)  # Invalidate cache
            return response.json()
        except requests.RequestException as e:
            print(f"Error completing tour: {e}")
            return None
