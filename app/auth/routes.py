from app.auth import auth_bp
from flask import render_template   


@auth_bp.route("/register")
def register():
    print(5)
    return render_template("auth/register.html")


@auth_bp.route("/login")
def login():
    return "Hello everyone I'm really tired!!!!"