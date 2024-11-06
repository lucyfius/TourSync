from flask import Flask, request, jsonify
from models import Base, Tour, TourStatus
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from config import DATABASE_URL

app = Flask(__name__)

# Database setup
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def check_time_conflict(session, tour_time, property_id, exclude_tour_id=None):
    """Check if there's a scheduling conflict"""
    query = session.query(Tour).filter(
        Tour.property_id == property_id,
        Tour.tour_time.between(tour_time - timedelta(hours=1), tour_time + timedelta(hours=1)),
        Tour.status == TourStatus.SCHEDULED
    )
    if exclude_tour_id:
        query = query.filter(Tour.id != exclude_tour_id)
    return query.first() is not None

@app.route('/api/tours', methods=['GET'])
def get_tours():
    session = Session()
    tours = session.query(Tour).all()
    return jsonify([tour.to_dict() for tour in tours])

@app.route('/api/tours', methods=['POST'])
def create_tour():
    session = Session()
    data = request.json
    
    tour_time = datetime.fromisoformat(data['tour_time'])
    
    if check_time_conflict(session, tour_time, data['property_id']):
        return jsonify({'error': 'Time slot conflict'}), 409
    
    new_tour = Tour(
        property_id=data['property_id'],
        tour_time=tour_time,
        client_name=data.get('client_name')
    )
    
    session.add(new_tour)
    session.commit()
    return jsonify(new_tour.to_dict()), 201

@app.route('/api/tours/<int:tour_id>', methods=['PUT'])
def update_tour_status(tour_id):
    session = Session()
    tour = session.query(Tour).get(tour_id)
    
    if not tour:
        return jsonify({'error': 'Tour not found'}), 404
    
    data = request.json
    new_status = TourStatus(data['status'])
    tour.status = new_status
    session.commit()
    
    return jsonify(tour.to_dict())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
