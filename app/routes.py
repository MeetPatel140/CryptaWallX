from flask import Flask, render_template, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = '6353877251'

@app.route('/')
def dashboard():
    flash("Welcome to your Dashboard !", "info")
    return render_template('dashboard.html')

@app.route('/login')
    flash("Logged-in Successfully !", "success")
    return render_template('dashboard.html', no_sidebar=True)

@app.route('/logout')
def logout():
    flash("Logged-out Successfully !", "success")
    return redirect(url_for('auth.login', no_sidebar=True))

@app.route('/signup')
def signup():
    flash("You are now Registered !", "success")
    return render_template('signup.html', no_sidebar=True)

@app.route('/reset-password')
def reset_password():
    flash("Password Reset instructions have been Sent !", "info")
    return render_template('reset_password.html', no_sidebar=True)

@app.route('/change-password')
def change_password():
    flash("Your Password has been Changed !", "success")
    return render_template('change_password.html', no_sidebar=True)

@app.route('/profile')
def profile():
    flash("Your Profile has been Updated !", "success")
    return render_template('profile.html')

@app.route('/delete-account')
def delete_account():
    flash("Your Account has been Deleted !", "success")
    return render_template('delete_account.html')

@app.errorhandler(404)
def page_not_found(e):
    flash("Not Found !", "danger")
    return render_template('404.html', no_sidebar=True), 404

@app.errorhandler(500)
def internal_server_error(e):
    flash("An error occurred. Please try again later.", "danger")
    return render_template('500.html', no_sidebar=True), 500

if __name__ == '__main__':
    app.run(debug=True)