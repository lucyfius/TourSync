from datetime import datetime
import re
from errors import ValidationError
from config import BUSINESS_HOURS, WORKING_DAYS

def validate_phone_number(phone):
    pattern = re.compile(r'^\+?1?\d{9,15}$')
    if not pattern.match(phone):
        raise ValidationError("Invalid phone number format")

def validate_tour_datetime(tour_time, end_time):
    if end_time <= tour_time:
        raise ValidationError("End time must be after tour time")
    
    if tour_time.weekday() not in WORKING_DAYS:
        raise ValidationError("Tours can only be scheduled Monday through Friday")
    
    hour = tour_time.hour
    if not (BUSINESS_HOURS['start'] <= hour < BUSINESS_HOURS['end']):
        raise ValidationError("Tour must be during business hours")

def validate_tour_data(tour_data):
    required_fields = ['property_id', 'tour_time', 'end_time', 'client_name', 'phone_number']
    for field in required_fields:
        if field not in tour_data:
            raise ValidationError(f"Missing required field: {field}")
    
    validate_phone_number(tour_data['phone_number'])
    validate_tour_datetime(tour_data['tour_time'], tour_data['end_time']) 