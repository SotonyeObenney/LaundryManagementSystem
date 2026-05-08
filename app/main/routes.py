from flask import render_template, redirect, url_for
from . import main_bp
from flask_login import current_user, login_required


@main_bp.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard_redirect'))
    return render_template("main/index.html")

@main_bp.route("/dashboard")
@login_required
def dashboard_redirect():
    if current_user.role == 'staff':
        return redirect(url_for('staff.dashboard'))
    return redirect(url_for("bookings.dashboard"))
