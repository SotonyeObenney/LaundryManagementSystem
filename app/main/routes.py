from flask import render_template, redirect, url_for
from . import main_bp


@main_bp.route("/")
def home():
    return "Welcome to our laundry service."


