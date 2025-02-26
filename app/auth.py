from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import User
from app import db
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# Define Blueprint
auth = Blueprint("auth", __name__)

# Register Form
class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

# Login Form
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

# Register Route
@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.confirm_password.data:
            flash('Passwords do not match. Please try again.', 'danger')
            return redirect(url_for('auth.register'))       
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already registered. Please log in.', 'warning')
            return redirect(url_for('auth.login'))
        
        # Create new user
        new_user = User(
            email=form.email.data,
            password=form.password.data  # Use the virtual property
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Registration Successful ! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html', form=form)

# Login Route
@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print(f"[DEBUG] Form submitted with email: {form.email.data}")

        user = User.query.filter_by(email=form.email.data).first()
        
        if user:
            print(f"[DEBUG] User found: {user.email}")
        else:
            print("[DEBUG] User not found in database")
        
        if user and user.check_password(form.password.data):
            print("[DEBUG] Password matched!")
            login_user(user)
            flash("Logged-in Successfully !", "success")
            return redirect(url_for("main.dashboard"))
        else:
            print("[DEBUG] Invalid email or password")
            flash("Invalid email or password !", "danger")

    return render_template("login.html", form=form)

# Logout Route
@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged-out Successfully !", "success")
    return redirect(url_for("auth.login", no_sidebar=True))
