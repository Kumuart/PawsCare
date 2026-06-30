from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.role == 'owner':
            return redirect(url_for('owner.dashboard'))
        elif current_user.role == 'vet_station':
            return redirect(url_for('vet.dashboard'))
        elif current_user.role == 'adoption_center':
            return redirect(url_for('adoption.dashboard'))
    return render_template('welcome.html')
