from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from models import (Pet, VetStation, Employee, Appointment, EmergencyRequest,
                    Medication, Vaccination, CommunityPost, CommunityComment,
                    AdoptionCenter, AdoptionPet, TimelineEvent)
from app import db
from datetime import datetime

owner_bp = Blueprint('owner', __name__)

def require_owner():
    if current_user.role != 'owner':
        return redirect(url_for('main.index'))

@owner_bp.route('/dashboard')
@login_required
def dashboard():
    require_owner()
    pets = Pet.query.filter_by(owner_id=current_user.id).all()
    upcoming_apts = Appointment.query.filter_by(owner_id=current_user.id)\
                    .filter(Appointment.status != 'rejected').order_by(Appointment.id.desc()).limit(3).all()
    active_meds = []
    for pet in pets:
        active_meds.extend(Medication.query.filter_by(pet_id=pet.id, active=True).all())
    return render_template('owner/dashboard.html', pets=pets,
                           appointments=upcoming_apts, active_meds=active_meds)

# ── My Pets ────────────────────────────────────────────────────
@owner_bp.route('/pets')
@login_required
def my_pets():
    pets = Pet.query.filter_by(owner_id=current_user.id).all()
    return render_template('owner/pets.html', pets=pets)

@owner_bp.route('/pets/<int:pet_id>')
@login_required
def pet_detail(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    medications = Medication.query.filter_by(pet_id=pet.id).all()
    vaccinations = Vaccination.query.filter_by(pet_id=pet.id).all()
    timeline = TimelineEvent.query.filter_by(pet_id=pet.id).order_by(TimelineEvent.date.desc()).all()
    emergencies = EmergencyRequest.query.filter_by(pet_id=pet.id).all()
    return render_template('owner/pet_detail.html', pet=pet, medications=medications,
                           vaccinations=vaccinations, timeline=timeline, emergencies=emergencies)

@owner_bp.route('/pets/add', methods=['GET', 'POST'])
@login_required
def add_pet():
    if request.method == 'POST':
        count = Pet.query.filter_by(owner_id=current_user.id).count()
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
            pet_pk=f'PET-{current_user.id}-{count+1:03d}'
        )
        db.session.add(pet)
        db.session.commit()
        flash('Pet profile created!', 'success')
        return redirect(url_for('owner.my_pets'))
    return render_template('owner/add_pet.html')

# ── Nearby Vets ────────────────────────────────────────────────
@owner_bp.route('/vets')
@login_required
def nearby_vets():
    filter_emergency = request.args.get('emergency')
    query = VetStation.query
    if filter_emergency:
        query = query.filter_by(emergency_available=True)
    stations = query.all()
    return render_template('owner/vets.html', stations=stations)

# ── Appointments ───────────────────────────────────────────────
@owner_bp.route('/appointments')
@login_required
def appointments():
    apts = Appointment.query.filter_by(owner_id=current_user.id)\
           .order_by(Appointment.id.desc()).all()
    stations = VetStation.query.all()
    pets = Pet.query.filter_by(owner_id=current_user.id).all()
    return render_template('owner/appointments.html', appointments=apts,
                           stations=stations, pets=pets)

@owner_bp.route('/appointments/book', methods=['GET', 'POST'])
@login_required
def book_appointment():
    if request.method == 'POST':
        apt = Appointment(
            owner_id=current_user.id,
            pet_id=int(request.form.get('pet_id')),
            station_id=int(request.form.get('station_id')),
            date=request.form.get('date'),
            time=request.form.get('time'),
            reason=request.form.get('reason'),
            status='pending'
        )
        db.session.add(apt)
        db.session.commit()
        flash('Appointment request sent!', 'success')
        return redirect(url_for('owner.appointments'))
    pets = Pet.query.filter_by(owner_id=current_user.id).all()
    stations = VetStation.query.all()
    return render_template('owner/book_appointment.html', pets=pets, stations=stations)

# ── Emergency ──────────────────────────────────────────────────
@owner_bp.route('/emergency')
@login_required
def emergency():
    pets = Pet.query.filter_by(owner_id=current_user.id).all()
    return render_template('owner/emergency.html', pets=pets)

@owner_bp.route('/emergency/submit', methods=['POST'])
@login_required
def emergency_submit():
    pet_id = int(request.form.get('pet_id'))
    q1 = request.form.get('q1', 'No')
    q2 = request.form.get('q2', '')
    q3 = request.form.get('q3', '')

    # Auto-score severity
    critical_keywords = ['Unconscious', 'Not Breathing', 'Bleeding Heavily']
    urgent_keywords = ['Seizure', 'Hit By Vehicle', 'Difficulty Breathing']

    severity = 'mild'
    if any(k in q1 or k in q2 for k in critical_keywords):
        severity = 'critical'
    elif any(k in q2 or k in q3 for k in urgent_keywords):
        severity = 'urgent'

    # Find nearest available station
    station = VetStation.query.filter_by(emergency_available=True).first()

    # Determine case type
    has_payment = current_user.payment_method_added
    has_station = station is not None

    if has_payment and has_station:
        case_type = 'case1' if severity == 'critical' else 'case2'
    else:
        case_type = 'case3'

    emg = EmergencyRequest(
        owner_id=current_user.id,
        pet_id=pet_id,
        station_id=station.id if station else None,
        severity=severity,
        symptoms_q1=q1,
        symptoms_q2=q2,
        symptoms_q3=q3,
        case_type=case_type,
        status='active',
        vet_eta='12 mins' if case_type == 'case1' else '5 mins',
        assigned_vet_id=station.employees[0].id if station and station.employees else None
    )
    db.session.add(emg)

    # Log to timeline
    pet = Pet.query.get(pet_id)
    tl = TimelineEvent(
        pet_id=pet_id,
        event_type='emergency',
        title=f'Emergency: {q2}',
        description=f'Severity: {severity.upper()}. Symptoms: {q3}',
        date=datetime.utcnow(),
        vet_name=station.employees[0].full_name if station and station.employees else 'AI Assistant'
    )
    db.session.add(tl)
    db.session.commit()

    return render_template('owner/emergency_result.html',
                           emergency=emg, station=station,
                           vet=station.employees[0] if station and station.employees else None,
                           case_type=case_type, severity=severity)

# ── Adoption ───────────────────────────────────────────────────
@owner_bp.route('/adoption')
@login_required
def adoption():
    centers = AdoptionCenter.query.all()
    available_pets = AdoptionPet.query.filter_by(status='available').all()
    return render_template('owner/adoption.html', centers=centers, pets=available_pets)

# ── Community ──────────────────────────────────────────────────
@owner_bp.route('/community')
@login_required
def community():
    posts = CommunityPost.query.order_by(CommunityPost.created_at.desc()).all()
    return render_template('owner/community.html', posts=posts)

@owner_bp.route('/community/post', methods=['POST'])
@login_required
def community_post():
    post = CommunityPost(
        author_id=current_user.id,
        display_name=request.form.get('display_name', current_user.full_name),
        title=request.form.get('title'),
        content=request.form.get('content'),
        post_type=request.form.get('post_type', 'general'),
        likes=0
    )
    db.session.add(post)
    db.session.commit()
    flash('Post shared to community!', 'success')
    return redirect(url_for('owner.community'))

@owner_bp.route('/community/<int:post_id>/comment', methods=['POST'])
@login_required
def add_comment(post_id):
    comment = CommunityComment(
        post_id=post_id,
        author_id=current_user.id,
        display_name=request.form.get('display_name', current_user.full_name),
        content=request.form.get('content')
    )
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('owner.community'))
