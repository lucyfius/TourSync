from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum
import logging

class TourStatus(str, Enum):
    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"

@dataclass
class TourState:
    id: str
    property_id: str
    tour_time: datetime
    end_time: datetime
    status: TourStatus
    client_name: str
    phone_number: str
    created_at: datetime
    updated_at: datetime

class StateManager:
    def __init__(self):
        self._tours: List[TourState] = []
        self._properties: List[dict] = []
        self._observers = []

    def add_observer(self, observer):
        self._observers.append(observer)

    def notify_observers(self):
        for observer in self._observers:
            observer()

    def validate_tour_data(self, tour_data: Dict[str, Any]) -> bool:
        """Validate tour data before creating TourState"""
        required_fields = {
            'id': str,
            'property_id': str,
            'tour_time': datetime,
            'end_time': datetime,
            'status': str,
            'client_name': str,
            'phone_number': str,
            'created_at': datetime,
            'updated_at': datetime
        }
        
        try:
            for field, field_type in required_fields.items():
                if field not in tour_data:
                    raise ValueError(f"Missing required field: {field}")
                if not isinstance(tour_data[field], field_type):
                    raise TypeError(f"Invalid type for {field}")
            return True
        except Exception as e:
            logging.error(f"Tour data validation failed: {e}")
            return False

    def update_tours(self, tours: List[Dict[str, Any]]) -> None:
        """Update tours with validation"""
        validated_tours = []
        for tour in tours:
            if self.validate_tour_data(tour):
                try:
                    validated_tours.append(TourState(**tour))
                except Exception as e:
                    logging.error(f"Failed to create TourState: {e}")
                    continue
        
        self._tours = validated_tours
        self.notify_observers()

    def get_tours(self):
        return self._tours

    def get_properties(self):
        return self._properties

    def update_properties(self, properties):
        self._properties = properties
        self.notify_observers() 