import requests

class ApiClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_tours(self):
        """Get all tours with error handling"""
        try:
            response = requests.get(f"{self.base_url}/tours")
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error fetching tours: {response.text}")
                return []
                
        except requests.exceptions.RequestException as e:
            print(f"Network error: {str(e)}")
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
                
        except requests.exceptions.RequestException as e:
            print(f"Network error: {str(e)}")
            return False