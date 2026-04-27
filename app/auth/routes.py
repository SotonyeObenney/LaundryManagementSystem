from ..auth import auth_bp
from flask import render_template, url_for, flash, redirect
from .forms import RegistrationForm, LoginForm   
from werkzeug.security import generate_password_hash
from ..models.user import User
from ..extensions import db

@auth_bp.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    # 1. THE FORM: Validate the form submission 
    if form.validate_on_submit():
        flash(f'Account created for {form.name.data}!', 'success')
        # 2. THE TRANSFORMATION: Hash the password before saving it to the database 
        hashed_password = generate_password_hash(form.password.data)
        
        # 3. THE MODEL: Create a new user instance with the form data and the hashed password
        new_user = User(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            address=form.address.data,
            password=hashed_password # Save the hash, NOT the raw password
        )
        
        # 4. THE DATABASE: Add the new user to the database and commit the transaction
        db.session.add(new_user)
        db.session.commit()
        
        # 5. THE FEEDBACK: Tell the user it worked and move them to login
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', form=form)
    



@auth_bp.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('auth/login.html', form=form)