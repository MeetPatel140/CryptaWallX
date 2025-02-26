from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import FirewallRule, NetworkAdapter
from app import db

main_bp = Blueprint("main", __name__)

# Dashboard route
@main_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

# Route for base.html (for layout structure)
@main_bp.route("/base")
def base():
    return render_template("base.html")

# Firewall management page
@main_bp.route("/firewall", methods=["GET", "POST"])
@login_required
def firewall():
    rules = FirewallRule.query.all()

    if request.method == "POST":
        rule_name = request.form.get("rule_name")
        action = request.form.get("action")
        protocol = request.form.get("protocol")
        port = request.form.get("port")
        ip_address = request.form.get("ip_address")

        # Validate input
        if not rule_name or not action or not protocol:
            flash("Rule name, action, and protocol are required!", "danger")
            return redirect(url_for("main.firewall"))

        # Create and save the rule
        rule = FirewallRule(
            rule_name=rule_name,
            action=action,
            protocol=protocol,
            port=port,
            ip_address=ip_address,
        )
        db.session.add(rule)
        db.session.commit()

        flash(f"Firewall rule '{rule_name}' added!", "success")
        return redirect(url_for("main.firewall"))

    return render_template("firewall.html", rules=rules)

# Profile page
@main_bp.route("/profile")
@login_required
def profile():
    return render_template("profile.html")

# Error handlers
@main_bp.app_errorhandler(404)
def page_not_found(e):
    flash("Page not found!", "danger")
    return render_template("404.html"), 404

@main_bp.app_errorhandler(500)
def internal_server_error(e):
    flash("Internal server error. Please try again later.", "danger")
    return render_template("500.html"), 500