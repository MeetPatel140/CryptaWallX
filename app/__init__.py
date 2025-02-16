from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, login_user, logout_user
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # Configuration settings
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost/cryptawallx"
    app.config['SECRET_KEY'] = "6353877251"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    Migrate(app, db)
    login_manager.init_app(app)

    # Set the login route for unauthenticated users
    login_manager.login_view = 'auth.login'

    from app.models import User  # Ensure models are imported

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Import and register the Blueprint correctly
    from app.auth import auth as auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    # Import the main Blueprint properly
    from app.main import main_bp
    app.register_blueprint(main_bp)

    # Ensure root URL redirects correctly
    @app.route("/")
    def index():
        if current_user.is_authenticated:
            return redirect(url_for("main.dashboard"))
        return redirect(url_for("auth.login"))

    return app
