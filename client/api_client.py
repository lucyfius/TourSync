from pymongo import MongoClient
import logging
from typing import Dict, List, Optional
from bson import ObjectId
from datetime import datetime
from .config import MONGODB_URI, MONGODB_DB

class ApiClient:
    def __init__(self):
        """Initialize MongoDB client"""
        self.client = MongoClient(MONGODB_URI)
        self.db = self.client[MONGODB_DB]

    # Tour Methods
    def add_tour(self, tour_data: Dict) -> Dict:
        """Add a new tour"""
        try:
            # Add creation timestamp
            tour_data['created_at'] = datetime.utcnow()
            tour_data['status'] = 'scheduled'
            
            result = self.db.tours.insert_one(tour_data)
            return {
                'success': True,
                'id': str(result.inserted_id)
            }
        except Exception as e:
            logging.error(f"Failed to add tour: {e}")
            return {
                'success': False,
                'error': str(e)
            }

    def get_tour(self, tour_id: str) -> Optional[Dict]:
        """Get a single tour by ID"""
        try:
            # Handle both string ID and dict with '_id'
            if isinstance(tour_id, dict) and '_id' in tour_id:
                tour_id = tour_id['_id']
                
            tour = self.db.tours.find_one({'_id': ObjectId(tour_id)})
            if tour:
                tour['_id'] = str(tour['_id'])
            return tour
        except Exception as e:
            logging.error(f"Failed to get tour: {e}")
            return None

    def get_tours(self) -> List[Dict]:
        """Fetch all tours"""
        try:
            tours = list(self.db.tours.find())
            # Convert ObjectId to string and ensure consistent ID field
            for tour in tours:
                tour['id'] = str(tour['_id'])  # Add 'id' field
                tour['_id'] = str(tour['_id'])  # Keep '_id' for compatibility
            return tours
        except Exception as e:
            logging.error(f"Failed to fetch tours: {e}")
            return []

    def update_tour(self, tour_id: str, tour_data: Dict) -> Dict:
        """Update an existing tour"""
        try:
            # Add update timestamp
            tour_data['updated_at'] = datetime.utcnow()
            
            result = self.db.tours.update_one(
                {'_id': ObjectId(tour_id)}, 
                {'$set': tour_data}
            )
            return {
                'success': True,
                'modified_count': result.modified_count
            }
        except Exception as e:
            logging.error(f"Failed to update tour: {e}")
            return {
                'success': False,
                'error': str(e)
            }

    def cancel_tour(self, tour_id: str, reason: str = None) -> Dict:
        """Cancel a tour"""
        return self.update_tour_status(tour_id, 'cancelled', reason)

    def complete_tour(self, tour_id: str, notes: str = None) -> Dict:
        """Mark a tour as completed"""
        return self.update_tour_status(tour_id, 'completed', notes)

    def delete_tour(self, tour_id: str) -> Dict:
        """Delete a tour"""
        try:
            # Extract ID from tour object if necessary
            if isinstance(tour_id, dict):
                tour_id = tour_id.get('id') or tour_id.get('_id')
            
            if not tour_id:
                raise ValueError("Invalid tour ID")

            result = self.db.tours.delete_one({'_id': ObjectId(tour_id)})
            return {
                'success': True,
                'deleted_count': result.deleted_count
            }
        except Exception as e:
            logging.error(f"Failed to delete tour: {e}")
            return {
                'success': False,
                'error': str(e)
            }

    def update_tour_status(self, tour_id: str, status: str, notes: str = None) -> Dict:
        """Update tour status
        
        Args:
            tour_id: Tour ID (can be string or dict containing '_id' or 'id')
            status: New status ('completed', 'cancelled', 'no_show', etc.)
            notes: Optional notes about the status change
            
        Returns:
            Dict with success/error information
        """
        try:
            # Extract ID from tour object if necessary
            if isinstance(tour_id, dict):
                tour_id = tour_id.get('id') or tour_id.get('_id')
            
            if not tour_id:
                raise ValueError("Invalid tour ID")

            # Prepare update data
            update_data = {
                'status': status,
                'updated_at': datetime.utcnow(),
                f'{status}_at': datetime.utcnow()
            }
            
            if notes:
                update_data[f'{status}_notes'] = notes

            result = self.db.tours.update_one(
                {'_id': ObjectId(tour_id)},
                {'$set': update_data}
            )
            
            return {
                'success': True,
                'modified_count': result.modified_count
            }
        except Exception as e:
            logging.error(f"Failed to update tour status: {e}")
            return {
                'success': False,
                'error': str(e)
            }

    # Property Methods
    def add_property(self, property_data: Dict) -> Dict:
        """Add a new property"""
        try:
            # Add creation timestamp
            property_data['created_at'] = datetime.utcnow()
            property_data['status'] = 'active'
            
            result = self.db.properties.insert_one(property_data)
            return {
                'success': True,
                'id': str(result.inserted_id)
            }
        except Exception as e:
            logging.error(f"Failed to add property: {e}")
            return {
                'success': False,
                'error': str(e)
            }

    def get_property(self, property_id: str) -> Optional[Dict]:
        """Get a single property by ID"""
        try:
            property_data = self.db.properties.find_one({'_id': ObjectId(property_id)})
            if property_data:
                property_data['_id'] = str(property_data['_id'])
            return property_data
        except Exception as e:
            logging.error(f"Failed to get property: {e}")
            return None

    def get_properties(self) -> List[Dict]:
        """Get all properties"""
        try:
            properties = list(self.db.properties.find({'status': 'active'}))
            for prop in properties:
                prop['_id'] = str(prop['_id'])
            return properties
        except Exception as e:
            logging.error(f"Failed to get properties: {e}")
            return []

    def update_property(self, property_id: str, property_data: Dict) -> Dict:
        """Update a property"""
        try:
            # Add update timestamp
            property_data['updated_at'] = datetime.utcnow()
            
            result = self.db.properties.update_one(
                {'_id': ObjectId(property_id)},
                {'$set': property_data}
            )
            return {
                'success': True,
                'modified_count': result.modified_count
            }
        except Exception as e:
            logging.error(f"Failed to update property: {e}")
            return {
                'success': False,
                'error': str(e)
            }

    def delete_property(self, property_id: str) -> Dict:
        """Delete a property (soft delete)"""
        try:
            # Check for active tours
            active_tours = self.db.tours.count_documents({
                'property_id': property_id,
                'status': {'$in': ['scheduled', 'pending']}
            })
            
            if active_tours > 0:
                return {
                    'success': False,
                    'error': f'Cannot delete property with {active_tours} active tours'
                }
            
            # Soft delete by updating status
            result = self.db.properties.update_one(
                {'_id': ObjectId(property_id)},
                {
                    '$set': {
                        'status': 'deleted',
                        'deleted_at': datetime.utcnow()
                    }
                }
            )
            return {
                'success': True,
                'modified_count': result.modified_count
            }
        except Exception as e:
            logging.error(f"Failed to delete property: {e}")
            return {
                'success': False,
                'error': str(e)
            }

    def mark_no_show(self, tour_id: str, notes: str = None) -> Dict:
        """Mark a tour as no-show"""
        return self.update_tour_status(tour_id, 'no_show', notes)