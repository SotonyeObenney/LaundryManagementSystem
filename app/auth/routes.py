from ..auth import auth_bp
from flask import render_template, url_for, flash, redirect
from flask_login import login_user, login_required, logout_user
from .forms import RegistrationForm, LoginForm   
from .. import bcrypt
from ..models import User
from ..extensions import db

@auth_bp.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    # 1. Validate the form submission 
    if form.validate_on_submit():
        password = form.password.data
        hashed_password = bcrypt.generate_password_hash(password=password).decode('utf-8') 
        new_user = User(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            address=form.address.data,
            password=hashed_password # Save the hash, NOT the raw password
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash(f'Account created for {form.name.data}!', 'success') 
        return redirect(url_for("auth.login")) # Change to dashboard later or remove login_user from line of above
    return render_template('auth/register.html', form=form)


@auth_bp.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.execute(db.select(User).where(User.email==form.email.data)).scalar()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login Successful!', 'success')
            return redirect(url_for('auth.register')) # Change to dashboard later
        flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('auth/login.html', form=form)

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.register"))  # Change to home page later
