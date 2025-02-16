from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import User
from app import db
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_login import login_required
from flask import render_template, redirect, url_for, flash, request
from app.forms import LoginForm  # Ensure this import is present



# Define a form for signup
class SignupForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")   

# Define the Blueprint correctly
auth = Blueprint("auth", __name__)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already exists. Please log in.', 'danger')
            return redirect(url_for('auth.login'))

        new_user = User(email=form.email.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template("signup.html", form=form)  # ✅ Pass form to template

@auth.route("/login", methods=["GET", "POST"])  # ✅ Fix: Use `auth`
def login():
    form = LoginForm()  # ✅ Initialize the form
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("main.dashboard"))  # Redirect to dashboard after login
        else:
            flash("Invalid email or password", "danger")

    return render_template("login.html")

@auth.route("/logout")  # ✅ Fix: Use `auth`
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))  # Redirect to login after logout
