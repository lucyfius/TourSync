from database import app, db
from models import Tour, TourStatus
from flask import request, jsonify
from datetime import datetime, timedelta

def check_time_conflict(tour_time, property_id, exclude_tour_id=None):
    """Check if there's a scheduling conflict"""
    query = Tour.query.filter(
        Tour.property_id == property_id,
        Tour.tour_time.between(tour_time - timedelta(hours=1), tour_time + timedelta(hours=1)),
        Tour.status == TourStatus.SCHEDULED
    )
    if exclude_tour_id:
        query = query.filter(Tour.id != exclude_tour_id)
    return query.first() is not None

@app.route('/api/tours', methods=['GET'])
def get_tours():
    tours = Tour.query.all()
    return jsonify([tour.to_dict() for tour in tours])

@app.route('/api/tours', methods=['POST'])
def create_tour():
    data = request.json
    
    tour_time = datetime.fromisoformat(data['tour_time'])
    
    if check_time_conflict(tour_time, data['property_id']):
        return jsonify({'error': 'Time slot conflict'}), 409
    
    new_tour = Tour(
        property_id=data['property_id'],
        tour_time=tour_time,
        client_name=data.get('client_name')
    )
    
    db.session.add(new_tour)
    db.session.commit()
    return jsonify(new_tour.to_dict()), 201

if __name__ == '__main__':
    app.run(debug=True)
