from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from models import VetStation, Employee, Pet, AdoptionPet, AdoptionCenter
from app import db

api_bp = Blueprint('api', __name__)

@api_bp.route('/vets')
@login_required
def get_vets():
    stations = VetStation.query.all()
    return jsonify([s.to_dict() for s in stations])

@api_bp.route('/vet/<int:station_id>/employees')
@login_required
def get_employees(station_id):
    emps = Employee.query.filter_by(station_id=station_id, available_today=True).all()
    return jsonify([e.to_dict() for e in emps])

@api_bp.route('/pets')
@login_required
def get_pets():
    if current_user.role == 'owner':
        pets = Pet.query.filter_by(owner_id=current_user.id).all()
        return jsonify([p.to_dict() for p in pets])
    return jsonify([])

@api_bp.route('/adoption/pets')
def get_adoption_pets():
    status = request.args.get('status', 'available')
    pets = AdoptionPet.query.filter_by(status=status).all()
    return jsonify([p.to_dict() for p in pets])

@api_bp.route('/post/<int:post_id>/like', methods=['POST'])
@login_required
def like_post(post_id):
    from models import CommunityPost
    post = CommunityPost.query.get_or_404(post_id)
    post.likes += 1
    db.session.commit()
    return jsonify({'likes': post.likes})
