from flask import Blueprint, request, jsonify
# from werkzeug.security import generate_password_hash, check_password_hash
from src.constants import http_status_codes
from src.database import db, User, Booking, Event, Booking 
import validators
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

booking = Blueprint("booking", __name__, url_prefix="/booking")


@booking.get('/all_events')
@jwt_required()
def all_events():
    
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 5))
    
    current_user = get_jwt_identity()
    user = User.query.filter_by(id=current_user).first()

    if not user:
        return jsonify({'message': 'User not found'}), http_status_codes.HTTP_404_NOT_FOUND

    events = Event.query.paginate(page=page, per_page=per_page, error_out=False)
    data = []

    for event in events.items:
        data.append({
            "id": event.id,
            'event_name': event.event_name,
            'event_date': event.event_date,
            'event_venue': event.event_venue,
            'available_seats': event.available_seats,
            'total_seats': event.total_seats,
            'event_time': event.event_time.strftime('%I:%M %p')
        })

    return jsonify({
        'events': data,
        'total_pages': events.pages,
        'total_events': events.total
    }), http_status_codes.HTTP_200_OK
