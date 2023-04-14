from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email, Length
import email_validator


class SignUpForm(FlaskForm):
    """Sign up form"""

    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('First name', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=6)])


class LoginForm(FlaskForm):
    """Login form"""

    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=6)])


class AddJobForm(FlaskForm):
    """Add new Job Form"""

    job_title = StringField("Job Title", validators=[DataRequired()])
    company_name = StringField("Company", validators=[DataRequired()])
    status = SelectField("Status", choices=[
                         'Wish list', 'Applied', "Interview", "Offer", "Rejected"])
