from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    # Configuration settings
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost/cryptawallx"
    app.config['SECRET_KEY'] = "6353877251"  # Use a stronger secret key in production
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize CSRF protection to protect against Cross-Site Request Forgery (CSRF) attacks
    csrf = CSRFProtect(app)

    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "warning"

    # Import the User model *AFTER* initializing db
    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Import and register blueprints
    from app.auth import auth as auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    from app.main import main_bp  # Import the Blueprint, not 'main'
    app.register_blueprint(main_bp)

    # Corrected import statement
    from app.bandwidth import bandwidth_bp  # Import the Blueprint, not 'bandwidth'
    app.register_blueprint(bandwidth_bp, url_prefix="/bandwidth")

    # Root URL redirection
    @app.route("/")
    def index():
        if current_user.is_authenticated:
            return redirect(url_for("main.dashboard"))
        return redirect(url_for("auth.login"))

    # Handle 404 errors
    @app.errorhandler(404)
    def page_not_found(e):
        return redirect(url_for("main.dashboard"))

    # Create database tables within the app context
    with app.app_context():
        db.create_all()

    return app