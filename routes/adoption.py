from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from models import AdoptionCenter, AdoptionPet
from app import db

adoption_bp = Blueprint('adoption', __name__)

def get_center():
    return AdoptionCenter.query.filter_by(user_id=current_user.id).first()

@adoption_bp.route('/dashboard')
@login_required
def dashboard():
    center = get_center()
    if not center:
        center = AdoptionCenter.query.first()
    available = AdoptionPet.query.filter_by(center_id=center.id, status='available').all()
    reserved = AdoptionPet.query.filter_by(center_id=center.id, status='reserved').all()
    adopted = AdoptionPet.query.filter_by(center_id=center.id, status='adopted').all()
    unavailable = AdoptionPet.query.filter_by(center_id=center.id, status='unavailable').all()
    return render_template('adoption/dashboard.html', center=center,
                           available=available, reserved=reserved,
                           adopted=adopted, unavailable=unavailable)

@adoption_bp.route('/pet/add', methods=['GET', 'POST'])
@login_required
def add_pet():
    center = get_center() or AdoptionCenter.query.first()
    if request.method == 'POST':
        count = AdoptionPet.query.filter_by(center_id=center.id).count()
        pet = AdoptionPet(
            center_id=center.id,
            name=request.form.get('name'),
            species=request.form.get('species'),
            breed=request.form.get('breed'),
            estimated_age=request.form.get('estimated_age'),
            gender=request.form.get('gender'),
            health_status=request.form.get('health_status'),
            status='available',
            description=request.form.get('description', ''),
            photo='🐾',
            pet_pk=f'AP-{center.id}-{count+1:03d}'
        )
        db.session.add(pet)
        db.session.commit()
        flash('Pet listing added!', 'success')
        return redirect(url_for('adoption.dashboard'))
    return render_template('adoption/add_pet.html', center=center)

@adoption_bp.route('/pet/<int:pet_id>/status', methods=['POST'])
@login_required
def update_status(pet_id):
    pet = AdoptionPet.query.get_or_404(pet_id)
    new_status = request.form.get('status')
    pet.status = new_status
    db.session.commit()
    flash(f'Pet status updated to {new_status}.', 'success')
    return redirect(url_for('adoption.dashboard'))

@adoption_bp.route('/pet/<int:pet_id>/remove', methods=['POST'])
@login_required
def remove_pet(pet_id):
    pet = AdoptionPet.query.get_or_404(pet_id)
    db.session.delete(pet)
    db.session.commit()
    flash('Pet listing removed.', 'success')
    return redirect(url_for('adoption.dashboard'))
