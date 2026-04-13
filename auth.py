from flask import Blueprint, request, render_template, redirect, url_for, flash
from werkzeug.security import check_password_hash
from flask_login import login_user # <-- Added Flask-Login

# Using a relative import to grab the User model from auth/models.py
from .models import User  

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # 1. Check if user exists
        user = User.query.filter_by(email=email).first()

        # 2. Validate user + password hash
        # Adjusted to match the likely database column name 'password_hash'
        if user and check_password_hash(user.password_hash, password):
            
            # 3. Log them in using Flask-Login
            login_user(user) 

            # Assuming the admin dashboard route is named 'dashboard'
            # and lives in an 'orders' or 'main' blueprint
            return redirect(url_for('dashboard'))  

        # 4. Invalid login case
        flash("Invalid email or password", "error")
        return redirect(url_for('auth.login'))

    # GET request - just show the page
    return render_template('auth/login.html') # <--  this has to match japheth and anu file path
