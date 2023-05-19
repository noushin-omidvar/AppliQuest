from wtforms import StringField, SelectField, ValidationError
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, TextAreaField, BooleanField, DateField, FileField, ValidationError, SubmitField
from wtforms.validators import DataRequired, Email, Length, URL, Regexp
from datetime import date
from models import Job, Company


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

    def valid_selection(form, field):
        if field.data == '':
            raise ValidationError('Please select a valid option.')

    job_title = StringField('Job Title', validators=[DataRequired()])
    company_name = StringField('Company', validators=[DataRequired()])
    status = SelectField('Status',
                         validators=[DataRequired(
                             message="Please select a status"), valid_selection],
                         choices=[('', ''),
                                  ('Wishlist', 'Wishlist'),
                                  ('Applied', 'Applied'),
                                  ('Interview', 'Interview'),
                                  ('Offer', 'Offer'),
                                  ('Rejected', 'Rejected')],
                         default='')


class JobDetailForm(FlaskForm):
    """Add new Job Form"""

    job_title = StringField("Job Title", validators=[DataRequired()])
    company_name = StringField("Company", validators=[DataRequired()])
    status = SelectField("Status", choices=[
                         'Wishlist', 'Applied', "Interview", "Offer", "Rejected"])
    post_url = StringField("Post URL", validators=[URL()])
    job_location = StringField("Location")
    notes = TextAreaField("Notes")
    job_description = TextAreaField("Description")


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
        self.company.choices = [(company.id, company.company_name)
                                for company in Company.query.all()]

    def validate(self):
        if not super().validate():
            return False

        # Set the job_id field based on the selected job
        company_id = self.job.data
        if company_id:
            self.company_id.data = company_id

        return True

    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    company = SelectField('Company', validators=[DataRequired()], render_kw={
        'placeholder': '+ Select Company'})
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[
        DataRequired(),
        Regexp(regex=r'^\+?[1-9]\d{1,14}$', message='Invalid phone number')])
    notes = TextAreaField("Notes")


class AddDocumentForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super(AddDocumentForm, self).__init__(*args, **kwargs)
        self.category.choices = ['Cover Letter',
                                 'Resume', 'Transcript', 'Certificate']

    document = FileField('Document', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    category = SelectField('Category')
    submit = SubmitField('Upload')
