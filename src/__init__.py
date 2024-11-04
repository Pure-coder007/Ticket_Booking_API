from flask import Flask, jsonify, redirect
import os
from flask_jwt_extended import JWTManager
from src.constants import http_status_codes
from src.database import db
from flask_migrate import Migrate
from src.auth import auth
# from src.booking import booking
# from src.admin import admin




def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    
    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DB_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JWT_SECRET_KEY=os.environ.get("JWT_SECRET_KEY")
        )
    else:
        app.config.from_mapping(test_config)
        
    db.init_app(app)
    migrate = Migrate(app, db)
    JWTManager(app)
    app.register_blueprint(auth)
    # app.register_blueprint(booking)    
    # app.register_blueprint(admin)    
    
    
    return app