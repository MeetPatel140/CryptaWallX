from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db

# User model with role support
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)  # Increased length to 255
    role = db.Column(db.String(50), nullable=False, default='user')  # Add a default role

    # Property to set the password (write-only)
    @property
    def password(self):
        raise AttributeError('Password is not readable!')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)  # Hash the password

    # Method to check the password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Bandwidth control rule model
class BandwidthRule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    adapter_name = db.Column(db.String(100), nullable=False)
    control_mode = db.Column(db.String(50), nullable=False)
    upload_limit = db.Column(db.Integer, default=0)  # Default to 0
    download_limit = db.Column(db.Integer, default=0)  # Default to 0
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

# Firewall rule model
class FirewallRule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rule_name = db.Column(db.String(255), nullable=False)
    action = db.Column(db.String(50), nullable=False)  # e.g., Allow, Block
    protocol = db.Column(db.String(50), nullable=True)  # e.g., TCP, UDP, ICMP
    port = db.Column(db.Integer, nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)  # IPv4/IPv6
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

# Network adapter model (for better management)
class NetworkAdapter(db.Model):
    __tablename__ = 'network_adapter'
    
    id = db.Column(db.Integer, primary_key=True)
    adapter_name = db.Column(db.String(255), nullable=False)
    adapter_type = db.Column(db.String(50))
    ip_address = db.Column(db.String(45))
    status = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())