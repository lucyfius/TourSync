from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from enum import Enum

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

    def update_tours(self, tours):
        self._tours = [TourState(**tour) for tour in tours]
        self.notify_observers()

    def get_tours(self):
        return self._tours

    def get_properties(self):
        return self._properties

    def update_properties(self, properties):
        self._properties = properties
        self.notify_observers() 