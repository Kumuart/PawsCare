from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from models import VetStation, Appointment, EmergencyRequest, Employee, Pet, User, TimelineEvent
from app import db
from datetime import datetime

vet_bp = Blueprint('vet', __name__)

def get_station():
    return VetStation.query.filter_by(user_id=current_user.id).first()

@vet_bp.route('/dashboard')
@login_required
def dashboard():
    station = get_station()
    if not station:
        # Demo: show first station
        station = VetStation.query.first()
    today_apts = Appointment.query.filter_by(station_id=station.id, status='accepted').limit(5).all()
    pending_apts = Appointment.query.filter_by(station_id=station.id, status='pending').all()
    emergencies = EmergencyRequest.query.filter_by(station_id=station.id, status='active').all()
    employees = Employee.query.filter_by(station_id=station.id).all()
    return render_template('vet/dashboard.html', station=station,
                           today_apts=today_apts, pending_apts=pending_apts,
                           emergencies=emergencies, employees=employees)

@vet_bp.route('/appointments')
@login_required
def appointments():
    station = get_station() or VetStation.query.first()
    apts = Appointment.query.filter_by(station_id=station.id)\
           .order_by(Appointment.id.desc()).all()
    return render_template('vet/appointments.html', appointments=apts, station=station)

@vet_bp.route('/appointment/<int:apt_id>/respond', methods=['POST'])
@login_required
def respond_appointment(apt_id):
    apt = Appointment.query.get_or_404(apt_id)
    action = request.form.get('action')
    apt.status = 'accepted' if action == 'accept' else 'rejected'
    db.session.commit()
    flash(f'Appointment {apt.status}.', 'success')
    return redirect(url_for('vet.appointments'))

@vet_bp.route('/emergencies')
@login_required
def emergencies():
    station = get_station() or VetStation.query.first()
    active = EmergencyRequest.query.filter_by(station_id=station.id, status='active').all()
    resolved = EmergencyRequest.query.filter_by(station_id=station.id, status='resolved').all()
    employees = Employee.query.filter_by(station_id=station.id, available_today=True, on_duty=True).all()
    return render_template('vet/emergencies.html', active=active, resolved=resolved,
                           employees=employees, station=station)

@vet_bp.route('/emergency/<int:emg_id>/assign', methods=['POST'])
@login_required
def assign_emergency(emg_id):
    emg = EmergencyRequest.query.get_or_404(emg_id)
    vet_id = request.form.get('vet_id')
    emg.assigned_vet_id = int(vet_id) if vet_id else None
    emg.status = 'assigned'
    # Add timeline entry
    tl = TimelineEvent(
        pet_id=emg.pet_id,
        event_type='emergency',
        title='Vet Assigned',
        description=f'Emergency assigned to vet. ETA: {emg.vet_eta}',
        date=datetime.utcnow(),
        vet_name='Dispatch'
    )
    db.session.add(tl)
    db.session.commit()
    flash('Vet assigned to emergency.', 'success')
    return redirect(url_for('vet.emergencies'))

@vet_bp.route('/employees')
@login_required
def employees():
    station = get_station() or VetStation.query.first()
    emps = Employee.query.filter_by(station_id=station.id).all()
    return render_template('vet/employees.html', employees=emps, station=station)

@vet_bp.route('/employee/<int:emp_id>/toggle', methods=['POST'])
@login_required
def toggle_duty(emp_id):
    emp = Employee.query.get_or_404(emp_id)
    field = request.form.get('field', 'on_duty')
    if field == 'on_duty':
        emp.on_duty = not emp.on_duty
    else:
        emp.available_today = not emp.available_today
    db.session.commit()
    flash('Status updated.', 'success')
    return redirect(url_for('vet.employees'))

@vet_bp.route('/records/<int:pet_id>', methods=['GET', 'POST'])
@login_required
def medical_records(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    from models import Medication, Vaccination
    if request.method == 'POST':
        entry_type = request.form.get('entry_type')
        if entry_type == 'medication':
            med = Medication(
                pet_id=pet.id,
                name=request.form.get('name'),
                dosage=request.form.get('dosage'),
                method=request.form.get('method'),
                duration=request.form.get('duration'),
                prescribed_by=request.form.get('prescribed_by', current_user.full_name),
                start_date=datetime.now().strftime('%Y-%m-%d'),
                active=True
            )
            db.session.add(med)
            tl = TimelineEvent(pet_id=pet.id, event_type='prescription',
                               title=f'Prescription: {med.name}', date=datetime.utcnow(),
                               vet_name=current_user.full_name,
                               description=f'{med.dosage} — {med.method} for {med.duration}')
            db.session.add(tl)
        elif entry_type == 'vaccination':
            vax = Vaccination(
                pet_id=pet.id,
                vaccine_name=request.form.get('vaccine_name'),
                date_given=request.form.get('date_given'),
                next_due=request.form.get('next_due'),
                administered_by=request.form.get('administered_by', current_user.full_name)
            )
            db.session.add(vax)
            tl = TimelineEvent(pet_id=pet.id, event_type='vaccination',
                               title=f'Vaccine: {vax.vaccine_name}', date=datetime.utcnow(),
                               vet_name=current_user.full_name,
                               description=f'Next due: {vax.next_due}')
            db.session.add(tl)
        db.session.commit()
        flash('Medical record added.', 'success')
    medications = pet.medications
    vaccinations = pet.vaccinations
    timeline = TimelineEvent.query.filter_by(pet_id=pet.id).order_by(TimelineEvent.date.desc()).all()
    return render_template('vet/records.html', pet=pet, medications=medications,
                           vaccinations=vaccinations, timeline=timeline)
