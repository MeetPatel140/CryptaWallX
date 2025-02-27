import subprocess
import logging
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.models import BandwidthRule
from app import db
from flask import jsonify
import random

bandwidth_bp = Blueprint('bandwidth', __name__)




def get_network_adapters():
    try:
        result = subprocess.run(['netsh', 'interface', 'show', 'interface'], capture_output=True, text=True)
        lines = result.stdout.splitlines()[3:]  # Skip the header lines
        adapters = []
        for line in lines:
            if line.strip():  # Skip empty lines
                parts = line.split()
                adapter_name = ' '.join(parts[3:])  # Adapter name is the last part
                adapters.append(adapter_name)
        return adapters
    except Exception as e:
        return [f"Error: {e}"]

@bandwidth_bp.route('/', methods=["GET", "POST"])
@login_required
def bandwidth_page():
    # Get real adapters from the system
    adapters = get_network_adapters()
    rules = BandwidthRule.query.all()

    if request.method == "POST":
        adapter_name = request.form.get("adapter_name")
        control_mode = request.form.get("control_mode")
        upload_limit = request.form.get("upload_limit")
        download_limit = request.form.get("download_limit")

        # Validate input
        if not adapter_name or not control_mode:
            flash("Adapter name and control mode are required!", "danger")
            return redirect(url_for("bandwidth.bandwidth_page"))

        # Convert empty strings to None (NULL in the database)
        upload_limit = int(upload_limit) if upload_limit else 0
        download_limit = int(download_limit) if download_limit else 0

        # Check if a rule for the same adapter already exists
        existing_rule = BandwidthRule.query.filter_by(adapter_name=adapter_name).first()

        if existing_rule:
            # Update the existing rule
            existing_rule.control_mode = control_mode
            existing_rule.upload_limit = upload_limit
            existing_rule.download_limit = download_limit
            flash(f"Bandwidth rule updated for {adapter_name}!", "success")
        else:
            # Create a new rule
            rule = BandwidthRule(
                adapter_name=adapter_name,
                control_mode=control_mode,
                upload_limit=upload_limit,
                download_limit=download_limit,
            )
            db.session.add(rule)
            flash(f"Bandwidth rule added for {adapter_name}!", "success")

        # Commit changes to the database
        db.session.commit()

        # Apply the bandwidth rule
        result = apply_bandwidth_rule(adapter_name, upload_limit, download_limit, control_mode)
        flash(result, "info")

        return redirect(url_for("bandwidth.bandwidth_page"))

    return render_template("bandwidth.html", adapters=adapters, rules=rules)

def apply_bandwidth_rule(adapter, upload_limit, download_limit, control_mode):
    try:
        if control_mode == "Unlimited":
            subprocess.run(['netsh', 'interface', 'ipv4', 'set', 'subinterface', adapter, 'mtu=0', 'store=persistent'])
            return f"Unlimited bandwidth set for {adapter}"

        if upload_limit or download_limit:
            # Ensure upload_limit and download_limit are valid integers
            upload_limit = upload_limit or 0
            download_limit = download_limit or 0

            command = [
                'netsh', 'interface', 'ipv4', 'set', 'subinterface', adapter,
                f"mtu={upload_limit}", "store=persistent"
            ]
            subprocess.run(command)
            return f"Bandwidth rule set for {adapter} - Upload: {upload_limit}Mbps, Download: {download_limit}Mbps"
        
        return f"Bandwidth rule set for {adapter}"
    
    except Exception as e:
        return f"Error: {e}"
    
@bandwidth_bp.route('/delete_rule/<int:rule_id>', methods=["POST"])
@login_required
def delete_bandwidth_rule(rule_id):
    rule = BandwidthRule.query.get_or_404(rule_id)
    db.session.delete(rule)
    db.session.commit()
    flash(f"Bandwidth rule for {rule.adapter_name} deleted!", "success")
    return redirect(url_for("bandwidth.bandwidth_page"))