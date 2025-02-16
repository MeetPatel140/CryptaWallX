from flask import Blueprint, render_template

# Create Blueprint
main_bp = Blueprint('main', __name__)

@main_bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')  # Ensure you have a `dashboard.html` file

