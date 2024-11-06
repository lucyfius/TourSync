from database import app, db
from models import Tour, TourStatus
from flask import request, jsonify
from datetime import datetime, timedelta
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import bleach
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure CORS
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:*"]}})

# Configure rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

def sanitize_input(data):
    """Sanitize input data to prevent XSS"""
    try:
        return {k: bleach.clean(str(v)) for k, v in data.items()}
    except Exception as e:
        logger.error(f"Error sanitizing input: {e}")
        raise ValueError("Invalid input data")

def check_time_conflict(tour_time, property_id, exclude_tour_id=None):
    """Check if there's a scheduling conflict"""
    try:
        query = Tour.query.filter(
            Tour.property_id == property_id,
            Tour.tour_time.between(tour_time - timedelta(hours=1), tour_time + timedelta(hours=1)),
            Tour.status == TourStatus.SCHEDULED
        )
        if exclude_tour_id:
            query = query.filter(Tour.id != exclude_tour_id)
        return query.first() is not None
    except Exception as e:
        logger.error(f"Error checking time conflict: {e}")
        raise

@app.errorhandler(429)
def ratelimit_handler(e):
    """Handle rate limit exceeded"""
    return jsonify(error="Rate limit exceeded. Please try again later."), 429

@app.errorhandler(Exception)
def handle_error(e):
    """Handle general errors"""
    logger.error(f"Unexpected error: {e}")
    return jsonify(error="An unexpected error occurred"), 500

@app.route('/api/tours', methods=['GET'])
def get_tours():
    try:
        tours = Tour.query.order_by(Tour.tour_time.desc()).all()
        return jsonify([tour.to_dict() for tour in tours])
    except Exception as e:
        logger.error(f"Error fetching tours: {e}")
        return jsonify(error="Failed to fetch tours"), 500

@app.route('/api/tours', methods=['POST'])
@limiter.limit("20 per minute")
def create_tour():
    try:
        if not request.json:
            return jsonify(error="Missing request data"), 400

        data = sanitize_input(request.json)
        
        # Validate required fields
        required_fields = ['tour_time', 'property_id', 'client_name']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify(error=f"Missing required fields: {', '.join(missing_fields)}"), 400

        try:
            tour_time = datetime.fromisoformat(data['tour_time'])
        except ValueError:
            return jsonify(error="Invalid tour time format"), 400
        
        if check_time_conflict(tour_time, data['property_id']):
            return jsonify(error='Time slot conflict'), 409
        
        new_tour = Tour(
            property_id=data['property_id'],
            tour_time=tour_time,
            client_name=data.get('client_name'),
            phone_number=data.get('phone_number')
        )
        
        db.session.add(new_tour)
        db.session.commit()
        
        logger.info(f"Created new tour: {new_tour.id}")
        return jsonify(new_tour.to_dict()), 201

    except ValueError as e:
        return jsonify(error=str(e)), 400
    except Exception as e:
        logger.error(f"Error creating tour: {e}")
        db.session.rollback()
        return jsonify(error="Failed to create tour"), 500

if __name__ == '__main__':
    app.run(debug=False)  # Set debug=False in production
