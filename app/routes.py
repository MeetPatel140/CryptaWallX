from flask import Flask, render_template, redirect, url_for, flash, request, jsonify, Blueprint
from flask_login import login_required, login_user, logout_user, current_user
from app import db
from app.models import User, BandwidthRule, FirewallRule, NetworkAdapter

# Main blueprint
main_bp = Blueprint('main', __name__)

# Dashboard route
@main_bp.route('/')
@login_required
def dashboard():
    flash("Welcome to your Dashboard!", "info")
    return render_template('dashboard.html')

# Login route
@main_bp.route('/login')
def login():
    flash("Logged-in Successfully!", "success")
    return render_template('dashboard.html', no_sidebar=True)

# Logout route
@main_bp.route('/logout')
def logout():
    logout_user()
    flash("Logged-out Successfully!", "success")
    return redirect(url_for('main.login'))

# Register route
@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.confirm_password.data:
            flash("Passwords do not match", "error")
            return redirect(url_for('main.register'))
        
        # Create new user
        new_user = User(email=form.email.data)
        new_user.password = form.password.data
        db.session.add(new_user)
        db.session.commit()
        
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('main.login'))
    return render_template('register.html', no_sidebar=True, form=form)

# Profile route
@main_bp.route('/profile')
@login_required
def profile():
    flash("Your profile has been updated!", "success")
    return render_template('profile.html')

# Bandwidth control management
@main_bp.route('/bandwidth', methods=['GET', 'POST'])
@login_required
def bandwidth():
    adapters = NetworkAdapter.query.all()
    rules = BandwidthRule.query.all()

    if request.method == 'POST':
        adapter_name = request.form.get('adapter_name')
        control_mode = request.form.get('control_mode')
        upload_limit = request.form.get('upload_limit')
        download_limit = request.form.get('download_limit')

        rule = BandwidthRule(
            adapter_name=adapter_name,
            control_mode=control_mode,
            upload_limit=upload_limit,
            download_limit=download_limit
        )
        db.session.add(rule)
        db.session.commit()

        flash(f"Bandwidth rule added for {adapter_name}!", "success")
        return redirect(url_for('main.bandwidth'))

    return render_template('bandwidth.html', adapters=adapters, rules=rules)

# Firewall management
@main_bp.route('/firewall', methods=['GET', 'POST'])
@login_required
def firewall():
    rules = FirewallRule.query.all()

    if request.method == 'POST':
        rule_name = request.form.get('rule_name')
        action = request.form.get('action')
        protocol = request.form.get('protocol')
        port = request.form.get('port')
        ip_address = request.form.get('ip_address')

        rule = FirewallRule(
            rule_name=rule_name,
            action=action,
            protocol=protocol,
            port=port,
            ip_address=ip_address
        )
        db.session.add(rule)
        db.session.commit()

        flash(f"Firewall rule '{rule_name}' added!", "success")
        return redirect(url_for('main.firewall'))

    return render_template('firewall.html', rules=rules)

# Delete account route
@main_bp.route('/delete-account')
@login_required
def delete_account():
    db.session.delete(current_user)
    db.session.commit()
    flash("Your account has been deleted!", "success")
    return redirect(url_for('main.login'))

# 404 error handler
@main_bp.app_errorhandler(404)
def page_not_found(e):
    flash("Page not found!", "danger")
    return render_template('404.html', no_sidebar=True), 404

# 500 error handler
@main_bp.app_errorhandler(500)
def internal_server_error(e):
    flash("An error occurred. Please try again later.", "danger")
    return render_template('500.html', no_sidebar=True), 500


@main_bp.route("/delete-bandwidth-rule/<int:rule_id>", methods=["POST"])
@login_required
def delete_bandwidth_rule(rule_id):
    rule = BandwidthRule.query.get_or_404(rule_id)
    db.session.delete(rule)
    db.session.commit()
    flash("Bandwidth rule deleted successfully!", "success")
    return redirect(url_for("main.bandwidth"))
