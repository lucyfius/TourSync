import requests
import logging
from typing import Dict, List, Optional
from .config import API_BASE_URL

class ApiClient:
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()

    def _handle_response(self, response: requests.Response) -> Dict:
        """Handle API response and errors"""
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"API request failed: {str(e)}")
            raise

    def get_tours(self) -> List[Dict]:
        """Fetch all tours"""
        response = self.session.get(f"{self.base_url}/tours")
        return self._handle_response(response)

    def create_tour(self, tour_data: Dict) -> Dict:
        """Create a new tour"""
        response = self.session.post(f"{self.base_url}/tours", json=tour_data)
        return self._handle_response(response)

    def update_tour(self, tour_id: str, tour_data: Dict) -> Dict:
        """Update an existing tour"""
        response = self.session.put(f"{self.base_url}/tours/{tour_id}", json=tour_data)
        return self._handle_response(response)

    def delete_tour(self, tour_id: str) -> Dict:
        """Delete a tour"""
        response = self.session.delete(f"{self.base_url}/tours/{tour_id}")
        return self._handle_response(response)