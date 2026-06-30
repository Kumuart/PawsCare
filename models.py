from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200))
    role = db.Column(db.String(20))  # owner, vet_station, adoption_center
    address = db.Column(db.String(200))
    gps_lat = db.Column(db.Float, default=-1.286389)
    gps_lng = db.Column(db.Float, default=36.817223)
    secondary_contact_name = db.Column(db.String(100))
    secondary_contact_phone = db.Column(db.String(20))
    secondary_contact_relation = db.Column(db.String(50))
    payment_method_added = db.Column(db.Boolean, default=False)
    card_last4 = db.Column(db.String(4))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    terms_accepted = db.Column(db.Boolean, default=False)
    avatar = db.Column(db.String(200), default='')

    pets = db.relationship('Pet', backref='owner', lazy=True)
    appointments = db.relationship('Appointment', backref='pet_owner', lazy=True,
                                   foreign_keys='Appointment.owner_id')
    emergency_requests = db.relationship('EmergencyRequest', backref='requester', lazy=True)
    community_posts = db.relationship('CommunityPost', backref='author', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'email': self.email,
            'role': self.role,
            'phone': self.phone,
            'address': self.address,
            'payment_method_added': self.payment_method_added,
        }


class Pet(db.Model):
    __tablename__ = 'pets'
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    species = db.Column(db.String(50))
    breed = db.Column(db.String(80))
    age = db.Column(db.String(20))
    gender = db.Column(db.String(10))
    weight = db.Column(db.String(20))
    known_conditions = db.Column(db.Text)
    allergies = db.Column(db.Text)
    photo = db.Column(db.String(200), default='')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    pet_pk = db.Column(db.String(20))

    medications = db.relationship('Medication', backref='pet', lazy=True)
    vaccinations = db.relationship('Vaccination', backref='pet', lazy=True)
    appointments = db.relationship('Appointment', backref='pet', lazy=True)
    emergency_requests = db.relationship('EmergencyRequest', backref='pet', lazy=True)
    timeline_events = db.relationship('TimelineEvent', backref='pet', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'species': self.species,
            'breed': self.breed,
            'age': self.age,
            'gender': self.gender,
            'weight': self.weight,
            'known_conditions': self.known_conditions,
            'allergies': self.allergies,
            'photo': self.photo,
        }


class TimelineEvent(db.Model):
    __tablename__ = 'timeline_events'
    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.id'), nullable=False)
    event_type = db.Column(db.String(50))  # vaccination, diagnosis, prescription, emergency, checkup
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    vet_name = db.Column(db.String(100))


class VetStation(db.Model):
    __tablename__ = 'vet_stations'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(150), nullable=False)
    address = db.Column(db.String(200))
    gps_lat = db.Column(db.Float, default=-1.286389)
    gps_lng = db.Column(db.Float, default=36.817223)
    photo = db.Column(db.String(200), default='')
    phone = db.Column(db.String(20))
    opening_hours = db.Column(db.String(20))
    closing_hours = db.Column(db.String(20))
    services = db.Column(db.Text)
    emergency_available = db.Column(db.Boolean, default=True)
    rating = db.Column(db.Float, default=4.5)
    station_pk = db.Column(db.String(20))

    employees = db.relationship('Employee', backref='station', lazy=True)
    appointments = db.relationship('Appointment', backref='vet_station', lazy=True)
    emergency_requests = db.relationship('EmergencyRequest', backref='assigned_station', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'phone': self.phone,
            'opening_hours': self.opening_hours,
            'closing_hours': self.closing_hours,
            'services': self.services,
            'emergency_available': self.emergency_available,
            'rating': self.rating,
            'photo': self.photo,
            'gps_lat': self.gps_lat,
            'gps_lng': self.gps_lng,
        }


class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    station_id = db.Column(db.Integer, db.ForeignKey('vet_stations.id'), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    gender = db.Column(db.String(10))
    years_experience = db.Column(db.Integer)
    specialty = db.Column(db.String(100))
    photo = db.Column(db.String(200), default='')
    available_today = db.Column(db.Boolean, default=True)
    on_duty = db.Column(db.Boolean, default=True)
    employee_pk = db.Column(db.String(20))

    def to_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'specialty': self.specialty,
            'years_experience': self.years_experience,
            'available_today': self.available_today,
            'on_duty': self.on_duty,
            'photo': self.photo,
        }


class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.id'), nullable=False)
    station_id = db.Column(db.Integer, db.ForeignKey('vet_stations.id'))
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    date = db.Column(db.String(20))
    time = db.Column(db.String(20))
    reason = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')  # pending, accepted, rejected, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    vet = db.relationship('Employee', backref='appointments')


class EmergencyRequest(db.Model):
    __tablename__ = 'emergency_requests'
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.id'), nullable=False)
    station_id = db.Column(db.Integer, db.ForeignKey('vet_stations.id'))
    severity = db.Column(db.String(20))   # critical, urgent, mild
    symptoms_q1 = db.Column(db.String(200))
    symptoms_q2 = db.Column(db.String(200))
    symptoms_q3 = db.Column(db.String(200))
    case_type = db.Column(db.String(20))  # case1, case2, case3
    status = db.Column(db.String(20), default='pending')
    vet_eta = db.Column(db.String(20))
    assigned_vet_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    assigned_vet = db.relationship('Employee', backref='emergencies')


class Medication(db.Model):
    __tablename__ = 'medications'
    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.id'), nullable=False)
    name = db.Column(db.String(100))
    dosage = db.Column(db.String(100))
    method = db.Column(db.String(80))
    duration = db.Column(db.String(80))
    prescribed_by = db.Column(db.String(100))
    start_date = db.Column(db.String(20))
    active = db.Column(db.Boolean, default=True)


class Vaccination(db.Model):
    __tablename__ = 'vaccinations'
    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.id'), nullable=False)
    vaccine_name = db.Column(db.String(100))
    date_given = db.Column(db.String(20))
    next_due = db.Column(db.String(20))
    administered_by = db.Column(db.String(100))


class AdoptionCenter(db.Model):
    __tablename__ = 'adoption_centers'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(150), nullable=False)
    address = db.Column(db.String(200))
    gps_lat = db.Column(db.Float, default=-1.286389)
    gps_lng = db.Column(db.Float, default=36.817223)
    photo = db.Column(db.String(200), default='')
    phone = db.Column(db.String(20))
    opening_hours = db.Column(db.String(20))
    closing_hours = db.Column(db.String(20))
    center_pk = db.Column(db.String(20))

    pets = db.relationship('AdoptionPet', backref='center', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'phone': self.phone,
            'opening_hours': self.opening_hours,
            'closing_hours': self.closing_hours,
            'photo': self.photo,
        }


class AdoptionPet(db.Model):
    __tablename__ = 'adoption_pets'
    id = db.Column(db.Integer, primary_key=True)
    center_id = db.Column(db.Integer, db.ForeignKey('adoption_centers.id'), nullable=False)
    name = db.Column(db.String(80))
    species = db.Column(db.String(50))
    breed = db.Column(db.String(80))
    estimated_age = db.Column(db.String(30))
    gender = db.Column(db.String(10))
    health_status = db.Column(db.String(80))  # Healthy, Requires Medication, Special Needs, Recovering
    status = db.Column(db.String(20), default='available')  # available, reserved, adopted, unavailable
    photo = db.Column(db.String(200), default='')
    description = db.Column(db.Text)
    pet_pk = db.Column(db.String(20))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'species': self.species,
            'breed': self.breed,
            'estimated_age': self.estimated_age,
            'gender': self.gender,
            'health_status': self.health_status,
            'status': self.status,
            'photo': self.photo,
            'description': self.description,
            'center_id': self.center_id,
        }


class CommunityPost(db.Model):
    __tablename__ = 'community_posts'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    display_name = db.Column(db.String(100))
    title = db.Column(db.String(200))
    content = db.Column(db.Text)
    post_type = db.Column(db.String(30), default='general')  # general, myth, question
    likes = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    comments = db.relationship('CommunityComment', backref='post', lazy=True)


class CommunityComment(db.Model):
    __tablename__ = 'community_comments'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('community_posts.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    display_name = db.Column(db.String(100))
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
