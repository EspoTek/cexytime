from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import app
from app.documents import User

# Register Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if email already exists
        if User.objects(email=email).first():
            flash('Email already registered.')
            return redirect(url_for('register'))

        # Hash the password and store the user
        password_hash = generate_password_hash(password)
        user = User(email=email, password_hash=password_hash)
        user.save()

        # Log the user in
        login_user(user)
        return redirect(url_for('index'))

    return render_template('register.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        remember = bool(request.form.get('remember'))

        # Find the user by email
        user = User.objects(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user, remember=remember)
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password.')
            return redirect(url_for('login'))

    return render_template('login.html')

# Logout Route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# ---------------------------------------------------------------------------
# Change password
# ---------------------------------------------------------------------------

@app.route('/change_password', methods=['POST'])
@login_required
def change_password():
    """Allow the logged-in user to change their account password."""
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')

    # Basic validations
    if new_password != confirm_password:
        flash('New password and confirmation do not match.', 'error')
        return redirect(url_for('settings'))

    if not check_password_hash(current_user.password_hash, current_password):
        flash('Current password is incorrect.', 'error')
        return redirect(url_for('settings'))

    # Everything looks good – update stored hash
    current_user.password_hash = generate_password_hash(new_password)
    current_user.save()

    flash('Your password has been updated.')
    return redirect(url_for('settings'))
