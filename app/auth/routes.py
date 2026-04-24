from app.auth import auth_bp
from flask import render_template, url_for, flash, redirect
from .forms import RegistrationForm, LoginForm   


@auth_bp.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    # This checks if the form was submitted AND if all validators passed
    if form.validate_on_submit():
        flash(f'Account created for {form.name.data}!', 'success')
        # Here is where you would normally create your User object:
        # new_user = User(name=form.name.data, email=form.email.data, ...)
        # db.session.add(new_user)
        # db.session.commit()
        return redirect(url_for('auth_bp.login')) 
    
    return render_template('auth/register.html', form=form)
    



@auth_bp.route("/login")
def login():
    return "Hello everyone I'm really tired!!!!"