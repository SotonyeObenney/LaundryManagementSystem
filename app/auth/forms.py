from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class RegistrationForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email(message="Invalid email address")])
    phone = StringField("Phone", validators=[DataRequired()])
    address = StringField("Address", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, message='Password must be at least 6 characters long')])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password"), Length(min=6)])
    # role  = StringField("Role", validators=[DataRequired()])
    # HTML code incase we want to add a dropdown for role selection in the future
    #  <div class="form-group">
    #         {{ form.role.label }} {{ form.role(class="form-control") }}
    #       </div>
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")