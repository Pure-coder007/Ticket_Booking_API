from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from src.constants import http_status_codes
from src.database import db, User, Booking, Event
import validators
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from datetime import datetime, time


admin = Blueprint("admin", __name__, url_prefix="/admin")




# Login admin
@admin.post('/login_admin')
def login():
    email = request.json.get('email', '')
    password = request.json.get('password', '')
    
    user = User.query.filter_by(email=email).first()
    
    if user:
        is_pass_correct = check_password_hash(user.password, password)
        
        if is_pass_correct and user.is_admin:
            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)
            return jsonify({'access_token': access_token, 'refresh_token': refresh_token, 'user': {'username': user.username, 'email': user.email}}), http_status_codes.HTTP_200_OK
    return jsonify({'message': 'Invalid email or password'}), http_status_codes.HTTP_401_UNAUTHORIZED










@admin.post('/add_event')
@jwt_required()
def add_event():
    admin_required = get_jwt_identity()
    
    if not admin_required:
        return jsonify({'message': 'Admin access required'}), http_status_codes.HTTP_401_UNAUTHORIZED
    
    # Fetch data from request
    event_name = request.json.get('event_name')
    event_date_str = request.json.get('event_date')
    event_time_str = request.json.get('event_time')
    event_venue = request.json.get('event_venue')
    total_seats = request.json.get('total_seats')
    available_seats = request.json.get('available_seats')
    
    # Check for missing fields
    if not all([event_name, event_date_str, event_time_str, event_venue, total_seats, available_seats]):
        return jsonify({'message': 'All fields are required'}), http_status_codes.HTTP_400_BAD_REQUEST
    
    # Convert date and time strings to appropriate types
    try:
        event_date = datetime.strptime(event_date_str, "%d %B %Y").date()  
        event_time = datetime.strptime(event_time_str, "%I%p").time()  
    except ValueError:
        return jsonify({'message': 'Invalid date or time format'}), http_status_codes.HTTP_400_BAD_REQUEST
    
    # Check that seats are integers and positive
    if not isinstance(total_seats, int) or not isinstance(available_seats, int):
        return jsonify({'message': 'Total seats and available seats must be integers'}), http_status_codes.HTTP_400_BAD_REQUEST
    
    if total_seats <= 0 or available_seats <= 0 or total_seats < available_seats:
        return jsonify({'message': 'Invalid seat counts'}), http_status_codes.HTTP_400_BAD_REQUEST
    
    # Create and add the event to the database
    event = Event(
        event_name=event_name, 
        event_date=event_date, 
        event_time=event_time, 
        event_venue=event_venue, 
        total_seats=total_seats, 
        available_seats=available_seats
    )
    db.session.add(event)
    db.session.commit()
    
    return jsonify({'message': 'Event added successfully'}), http_status_codes.HTTP_201_CREATED




# from datetime import datetime, time
# from flask import request, jsonify
# from flask_jwt_extended import jwt_required, get_jwt_identity

@admin.put('/update_event/<event_id>')
@jwt_required()
def update_event(event_id):
    admin_required = get_jwt_identity()
    
    if not admin_required:
        return jsonify({'message': 'Admin access required'}), http_status_codes.HTTP_401_UNAUTHORIZED
    
    event = Event.query.get_or_404(event_id)

    try:
        event.event_name = request.json.get('event_name', event.event_name)
        
        # Update event_date
        event_date_str = request.json.get('event_date', event.event_date)
        if event_date_str:
            event.event_date = datetime.strptime(event_date_str, '%d %B %Y')  # Adjust format as needed
        
        # Update event_time
        event_time_str = request.json.get('event_time', event.event_time)
        if event_time_str:
            # Convert '2pm' or similar formats to a time object
            event_time_obj = datetime.strptime(event_time_str, '%I%p').time()  # Adjust format as needed
            event.event_time = event_time_obj
        
        event.event_venue = request.json.get('event_venue', event.event_venue)
        event.total_seats = request.json.get('total_seats', event.total_seats)
        event.available_seats = request.json.get('available_seats', event.available_seats)
        
        db.session.commit()
        
        return jsonify({'message': 'Event updated successfully'}), http_status_codes.HTTP_200_OK

    except ValueError as ve:
        return jsonify({'message': str(ve)}), 400
    except Exception as e:
        return jsonify({'message': str(e)}), 500







# Delete Event
@admin.delete('/delete_event/<event_id>')
@jwt_required()
def delete_event(event_id):
    admin_required = get_jwt_identity()
    
    if not admin_required:
        return jsonify({'message': 'Admin access required'}), http_status_codes.HTTP_401_UNAUTHORIZED
    
    
    
    event = Event.query.get(event_id)
    if not event:
        return jsonify({'message': 'Event not found'}), http_status_codes.HTTP_404_NOT_FOUND
    db.session.delete(event)
    db.session.commit()
    
    return jsonify({'message': 'Event deleted successfully'}), http_status_codes.HTTP_200_OK