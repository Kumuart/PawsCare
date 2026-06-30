from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'pawscare-hackathon-2025-secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pawscare.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from routes.auth import auth_bp
    from routes.owner import owner_bp
    from routes.vet import vet_bp
    from routes.adoption import adoption_bp
    from routes.main import main_bp
    from routes.api import api_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(owner_bp, url_prefix='/owner')
    app.register_blueprint(vet_bp, url_prefix='/vet')
    app.register_blueprint(adoption_bp, url_prefix='/adoption')
    app.register_blueprint(api_bp, url_prefix='/api')

    with app.app_context():
        from models import User, Pet, VetStation, Employee, AdoptionCenter, AdoptionPet
        from models import Appointment, EmergencyRequest, Medication, Vaccination, CommunityPost
        db.create_all()
        from seed import seed_data
        seed_data(db)

    return app
