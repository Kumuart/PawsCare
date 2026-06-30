from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from models import User, Pet, VetStation, AdoptionCenter
from app import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/welcome')
def welcome():
    return render_template('welcome.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    role = request.args.get('role', 'owner')
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            if user.role == 'owner':
                return redirect(url_for('owner.dashboard'))
            elif user.role == 'vet_station':
                return redirect(url_for('vet.dashboard'))
            elif user.role == 'adoption_center':
                return redirect(url_for('adoption.dashboard'))
        else:
            flash('Invalid email or password.', 'error')
    return render_template('auth/login.html', role=role)

@auth_bp.route('/register/<role>', methods=['GET', 'POST'])
def register(role):
    if request.method == 'POST':
        email = request.form.get('email')
        if User.query.filter_by(email=email).first():
            flash('Email already in use.', 'error')
            return render_template('auth/register.html', role=role)

        user = User(
            full_name=request.form.get('full_name'),
            phone=request.form.get('phone'),
            email=email,
            role=role,
            address=request.form.get('address', ''),
            terms_accepted=True
        )
        user.set_password(request.form.get('password'))
        db.session.add(user)
        db.session.commit()
        login_user(user)

        if role == 'owner':
            return redirect(url_for('auth.create_pet'))
        elif role == 'vet_station':
            return redirect(url_for('auth.setup_station'))
        elif role == 'adoption_center':
            return redirect(url_for('auth.setup_center'))

    return render_template('auth/register.html', role=role)

@auth_bp.route('/create-pet', methods=['GET', 'POST'])
@login_required
def create_pet():
    if request.method == 'POST':
        pet = Pet(
            owner_id=current_user.id,
            name=request.form.get('name'),
            species=request.form.get('species'),
            breed=request.form.get('breed'),
            age=request.form.get('age'),
            gender=request.form.get('gender'),
            weight=request.form.get('weight'),
            known_conditions=request.form.get('known_conditions'),
            allergies=request.form.get('allergies'),
            photo='🐾',
            pet_pk=f'PET-{current_user.id}-001'
        )
        db.session.add(pet)
        db.session.commit()
        return redirect(url_for('owner.dashboard'))
    return render_template('auth/create_pet.html')

@auth_bp.route('/setup-station', methods=['GET', 'POST'])
@login_required
def setup_station():
    if request.method == 'POST':
        s = VetStation(
            user_id=current_user.id,
            name=request.form.get('name'),
            address=request.form.get('address'),
            phone=request.form.get('phone'),
            opening_hours=request.form.get('opening_hours'),
            closing_hours=request.form.get('closing_hours'),
            services=request.form.get('services'),
            emergency_available='emergency' in request.form,
            station_pk=f'VS-{current_user.id}'
        )
        db.session.add(s)
        db.session.commit()
        return redirect(url_for('vet.dashboard'))
    return render_template('auth/setup_station.html')

@auth_bp.route('/setup-center', methods=['GET', 'POST'])
@login_required
def setup_center():
    if request.method == 'POST':
        c = AdoptionCenter(
            user_id=current_user.id,
            name=request.form.get('name'),
            address=request.form.get('address'),
            phone=request.form.get('phone'),
            opening_hours=request.form.get('opening_hours'),
            closing_hours=request.form.get('closing_hours'),
            center_pk=f'AC-{current_user.id}'
        )
        db.session.add(c)
        db.session.commit()
        return redirect(url_for('adoption.dashboard'))
    return render_template('auth/setup_center.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
