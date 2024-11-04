from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from src.constants import http_status_codes
from src.database import db, User, Booking, Event
import validators
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.post('/register')
def register():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    
    if len(username) < 3:
        return jsonify({'message': 'Username must be at least 3 characters long'}), http_status_codes.HTTP_400_BAD_REQUEST
    
    if len(password) < 6:
        return jsonify({'message': 'Password must be at least 6 characters long'}), http_status_codes.HTTP_400_BAD_REQUEST
    
    if not validators.email(email):
        return jsonify({'message': 'Email is not valid'}), http_status_codes.HTTP_400_BAD_REQUEST
    
    if User.query.filter_by(email=email).first() is not None:
        return jsonify({'message': 'Email already exists'}), http_status_codes.HTTP_400_BAD_REQUEST
    
    if User.query.filter_by(username=username).first() is not None:
        return jsonify({'message': 'Username already exists'}), http_status_codes.HTTP_400_BAD_REQUEST
    
    password_hash = generate_password_hash(password)
    user = User(username=username, email=email, password=password_hash, is_admin=False)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully', 'user': {'username': user.username, 'email': user.email}}), http_status_codes.HTTP_201_CREATED
    
    
    



@auth.post('/login')
def login():
    email = request.json.get('email', '')
    password = request.json.get('password', '')
    
    user = User.query.filter_by(email=email).first()
    
    if user:
        is_pass_correct = check_password_hash(user.password, password)
        
        if is_pass_correct:
            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)
            return jsonify({'access_token': access_token, 'refresh_token': refresh_token, 'user': {'username': user.username, 'email': user.email}}), http_status_codes.HTTP_200_OK
    return jsonify({'message': 'Invalid email or password'}), http_status_codes.HTTP_401_UNAUTHORIZED



# View Profile and booked events
@auth.get('/user_profile')
@jwt_required()
def user_profile():
    current_user = get_jwt_identity()
    user = User.query.filter_by(id=current_user).first()
    booked_events = Booking.query.filter_by(user_id=current_user).all()
    
    
    if user and booked_events:
        return jsonify({'user': {'username': user.username, 'email': user.email}, 'booked_events': [event.event_name for event in booked_events]}), http_status_codes.HTTP_200_OK
    return jsonify({'user': {'username': user.username, 'email': user.email}, 'booked_events': [] }), http_status_codes.HTTP_404_NOT_FOUND



