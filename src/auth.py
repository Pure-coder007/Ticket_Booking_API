from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from src.constants import http_status_codes
from src.database import db, User
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
    
    