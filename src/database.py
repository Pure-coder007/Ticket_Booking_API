from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import string
import random

db = SQLAlchemy()

# ID generator
def random_id():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(20))

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(50), primary_key=True, default=random_id)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)  
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 
    is_admin = db.Column(db.Boolean, default=False)

    # Relationship with Booking
    bookings = db.relationship('Booking', back_populates='user', lazy=True)  
    
    def __repr__(self) -> str:
        return f'<User {self.username}>'

class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.String(50), primary_key=True, default=random_id)  
    user_id = db.Column(db.String(50), db.ForeignKey('users.id'), nullable=False)  
    event_id = db.Column(db.String(50), db.ForeignKey('events.id'), nullable=False)  
    event_name = db.Column(db.String(100), nullable=False)
    booking_date = db.Column(db.DateTime, default=datetime.utcnow) 
    ticket_count = db.Column(db.Integer, nullable=False)  
    status = db.Column(db.String(20), default='confirmed')  
    
    # Relationships with User and Event
    user = db.relationship('User', back_populates='bookings')  
    event = db.relationship('Event', back_populates='bookings')  

    def __repr__(self):
        return f'<Booking {self.id} - User {self.user_id} - Event {self.event_id}>'
    
class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.String(50), primary_key=True, default=random_id)  
    event_name = db.Column(db.String(100), nullable=False) 
    event_date = db.Column(db.DateTime, nullable=False)  
    event_venue = db.Column(db.String(100), nullable=False) 
    total_seats = db.Column(db.Integer, nullable=False)  
    available_seats = db.Column(db.Integer, nullable=False)  
    event_time = db.Column(db.Time, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow) 
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  

    # Relationship with Booking
    bookings = db.relationship('Booking', back_populates='event', lazy=True)  

    def __repr__(self):
        return f'<Event {self.event_name} - Date: {self.event_date}>'
