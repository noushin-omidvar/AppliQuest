from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, TextAreaField, BooleanField, DateField
from wtforms.validators import DataRequired, Email, Length, URL
from datetime import date
from models import Job


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
                         'Wishlist', 'Applied', "Interview", "Offer", "Rejected"])


class JobDetailForm(FlaskForm):
    """Add new Job Form"""

    job_title = StringField("Job Title", validators=[DataRequired()])
    company_name = StringField("Company", validators=[DataRequired()])
    status = SelectField("Status", choices=[
                         'Wishlist', 'Applied', "Interview", "Offer", "Rejected"])
    post_url = StringField("Post URL", validators=[URL()])
    location = StringField("Location")
    notes = TextAreaField("Notes")


class AddTaskForm(FlaskForm):
    """Add new task form"""

    def __init__(self, *args, **kwargs):
        super(AddTaskForm, self).__init__(*args, **kwargs)
        self.job.choices = [(job.id, job.job_title) for job in Job.query.all()]

    def validate(self):
        if not super().validate():
            return False

        # Set the job_id field based on the selected job
        job_id = self.job.data
        if job_id:
            self.job_id.data = job_id

        return True

    task = StringField("Title", validators=[DataRequired()])
    job = SelectField('Job', validators=[DataRequired()], render_kw={
                      'placeholder': '+ Link to Job'})
    startdate = DateField('Start Date', default=date.today)
    enddate = DateField('End Date', default=date.today)
    notes = TextAreaField("Notes")
    completed = BooleanField("Mark as Completed")


class AddContactForm(FlaskForm):
    """Add new contact form"""

    def __init__(self, *args, **kwargs):
        super(AddContactForm, self).__init__(*args, **kwargs)
        self.job.choices = [(job.id, job.job_title) for job in Job.query.all()]

    def validate(self):
        if not super().validate():
            return False

        # Set the job_id field based on the selected job
        job_id = self.job.data
        if job_id:
            self.job_id.data = job_id

        return True

    contact = StringField("Title", validators=[DataRequired()])
    job = SelectField('Job', validators=[DataRequired()], render_kw={
                      'placeholder': '+ Link to Job'})
    startdate = DateField('Start Date', default=date.today)
    enddate = DateField('End Date', default=date.today)
    notes = TextAreaField("Notes")
    completed = BooleanField("Mark as Completed")
