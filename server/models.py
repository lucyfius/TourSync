from datetime import datetime
from database import db
import enum

class TourStatus(enum.Enum):
    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    NO_SHOW = "no_show"

class Tour(db.Model):
    __tablename__ = 'tours'
    
    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.String(50), nullable=False)
    tour_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum(TourStatus), default=TourStatus.SCHEDULED)
    client_name = db.Column(db.String(100))
    phone_number = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Add indexes for frequently queried columns
    __table_args__ = (
        db.Index('idx_tour_time', 'tour_time'),
        db.Index('idx_property_status', 'property_id', 'status'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'property_id': self.property_id,
            'tour_time': self.tour_time.isoformat(),
            'status': self.status.value,
            'client_name': self.client_name,
            'phone_number': self.phone_number,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
