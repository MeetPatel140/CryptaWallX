from flask import Flask, render_template, redirect, url_for, flash, request, jsonify, Blueprint

app = Flask(__name__)
app.secret_key = '6353877251'

# Dashboard route
@app.route('/')
def dashboard():
    flash("Welcome to your Dashboard!", "info")
    return render_template('dashboard.html')

# Login route
@app.route('/login')
def login():
    flash("Logged-in Successfully!", "success")
    return render_template('dashboard.html', no_sidebar=True)

# Logout route
@app.route('/logout')
def logout():
    flash("Logged-out Successfully!", "success")
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.confirm_password.data:
            flash("Passwords do not match", "error")
            return redirect(url_for('register', no_sidebar=True))
        # If passwords match, proceed with registration logic
        flash("Registration successful!", "success")
        return redirect(url_for('login'))
    return render_template('register.html', no_sidebar=True, form=form)

# Reset password route
@app.route('/reset-password')
def reset_password():
    flash("Password reset instructions have been sent!", "info")
    return render_template('reset_password.html', no_sidebar=True)

# Change password route
@app.route('/change-password')
def change_password():
    flash("Your password has been changed!", "success")
    return render_template('change_password.html', no_sidebar=True)

# Profile route
@app.route('/profile')
def profile():
    flash("Your profile has been updated!", "success")
    return render_template('profile.html')

# Delete account route
@app.route('/delete-account')
def delete_account():
    flash("Your account has been deleted!", "success")
    return render_template('delete_account.html')

# 404 error handler
@app.errorhandler(404)
def page_not_found(e):
    flash("Page not found!", "danger")
    return render_template('404.html', no_sidebar=True), 404

# 500 error handler
@app.errorhandler(500)
def internal_server_error(e):
    flash("An error occurred. Please try again later.", "danger")
    return render_template('500.html', no_sidebar=True), 500

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
