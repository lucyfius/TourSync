import requests
from datetime import datetime
from config import API_BASE_URL

class TourAPIClient:
    def __init__(self):
        self.base_url = API_BASE_URL
        self.session = requests.Session()
        self.cache = {}

    def get_tours(self):
        """Fetch all tours with caching"""
        cache_key = 'tours'
        if cache_key in self.cache:
            return self.cache[cache_key]
            
        try:
            response = self.session.get(f"{self.base_url}/tours")
            response.raise_for_status()
            tours = response.json()
            self.cache[cache_key] = tours
            return tours
        except requests.RequestException as e:
            print(f"Error fetching tours: {e}")
            return []

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
