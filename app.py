import os
import googlemaps
from flask import Flask, render_template, session, g, redirect, flash, jsonify, request
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from models import db, connect_db, User, Job, Company, Document, Task, Contact
from forms import SignUpForm, LoginForm, AddJobForm, JobDetailForm, AddTaskForm, TaskDetailForm, AddContactForm, detailContactForm, AddDocumentForm, detailDocumentForm
from datetime import date, datetime
from api import api_bp


CURR_USER_KEY = "curr_user_id"

app = Flask(__name__)
app.register_blueprint(api_bp, url_prefix='/api/v1')
# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use the provided database URL.
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'postgresql:///appliquest')  # 'postgresql://admin:zXRwj5Htsme5Wbwz9ztFX2odGy4Qyiyd@dpg-cilir05ph6eg6k9oj4eg-a/appliquest')


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
toolbar = DebugToolbarExtension(app)

connect_db(app)
with app.app_context():
    db.create_all()


# ------------------------
# Set up view endpoints
# ------------------------

# -------------------------
# User signup/login/logout
# -------------------------


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.
    Create new user and add to DB. Redirect to home page.
    If form not valid, present form.
    If the there already is a user with that email: flash message
    and re-present form.
    """

    if g.user:
        return redirect("/")

    form = SignUpForm()
    if form.validate_on_submit():
        try:
            user = User.signup(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                password=form.password.data,
                email=form.email.data,
                linkedin_url=None,
                user_location=None
            )
            db.session.commit()
            do_login(user)
            return redirect('/')

        except IntegrityError:
            flash("An account already exists with this email", 'danger')
            return render_template('users/signup.html', form=form)

    return render_template('users/signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.email.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.first_name}!", "success")
            return jsonify({'user_id': user.id})

        flash("Invalid credentials.", 'danger')

    return render_template('users/login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()
    flash("You have been loged out", "info")

    return redirect('/')

# ------------------------
# Define general routes
# -------------------------


@app.route('/')
def index():
    """ Home page """
    if not g.user:
        return render_template('index.html')

    return redirect('/board')


@app.route('/board')
def show_board():
    """Job tracking board"""

    if not g.user:
        return render_template('index.html')

    new_job_form = AddJobForm()
    job_detail_form = JobDetailForm()
    print(g.user.id)
    jobs = {'jobs_wished': Job.get_jobs_by_status(g.user.id, "Wishlist"),
            'jobs_applied': Job.get_jobs_by_status(g.user.id, "Applied"),
            'jobs_interview': Job.get_jobs_by_status(g.user.id, "Interview"),
            'jobs_offer': Job.get_jobs_by_status(g.user.id, "Offer"),
            'jobs_rejected': Job.get_jobs_by_status(g.user.id, "Rejected"), }

    print(jobs)
    return render_template('users/board.html', user_id=g.user.id,
                           jobs=jobs,
                           new_job_form=new_job_form,
                           job_detail_form=job_detail_form,
                           datetime=datetime)


@app.route('/tasks')
def show_tasks():
    """Job tracking board"""

    if not g.user:
        return render_template('index.html')

    jobs = Job.query.filter(Job.user_id == g.user.id).all()
    new_task_form = AddTaskForm(jobs)
    task_detail_form = TaskDetailForm(jobs)

    tasks = {'All': Task.query.filter(Task.user_id == g.user.id).all(),
             'Due-Today': Task.query.filter(Task.user_id == g.user.id, Task.due_date == date.today()).all(),
             'Past-Due': Task.query.filter(Task.user_id == g.user.id, Task.due_date < date.today()).all(),
             'Completed': Task.query.filter(Task.user_id == g.user.id, Task.completed == True).all(),

             'Wishlists': Task.query.join(Job).filter(Task.user_id == g.user.id, Job.status == 'Wishlist').all(),
             'Applications': Task.query.join(Job).filter(Task.user_id == g.user.id, Job.status == 'Applied').all(),
             'Interviews': Task.query.join(Job).filter(Task.user_id == g.user.id, Job.status == 'Interview').all(),
             'Offers': Task.query.join(Job).filter(Task.user_id == g.user.id, Job.status == 'Offer').all(),
             'Rejections': Task.query.join(Job).filter(Task.user_id == g.user.id, Job.status == 'Rejected').all(),
             }
    return render_template('users/tasks.html', user_id=g.user.id,
                           tasks=tasks,
                           new_task_form=new_task_form,
                           task_detail_form=task_detail_form)


@app.route('/contacts')
def show_contacts():
    if not g.user:
        return render_template('index.html')

    contacts = Contact.query.filter(Contact.user_id == g.user.id).all()
    new_contact_form = AddContactForm()
    detail_contact_form = detailContactForm()
    return render_template('users/contacts.html',
                           contacts=contacts,
                           new_contact_form=new_contact_form,
                           detail_contact_form=detail_contact_form)


@app.route('/documents')
def show_documents():
    if not g.user:
        return render_template('index.html')

    documents = Document.query.filter(Document.user_id == g.user.id).all()
    new_document_form = AddDocumentForm()
    detail_document_form = detailDocumentForm()
    return render_template('users/documents.html',
                           documents=documents,
                           new_document_form=new_document_form,
                           detail_document_form=detail_document_form,
                           datetime=date)


@app.route('/map')
def show_map():
    if not g.user:
        return render_template('index.html')
    google_map_api_key = os.environ.get('GOOGLE_MAP_API_KEY')
    gmaps = googlemaps.Client(api_key=google_map_api_key)

    user_jobs = Job.query.filter_by(user_id=g.user.id).all()
    job_locations = [job.job_location for job in user_jobs if job.job_location]
    marker_locations = []
    for city in job_locations:
        geocode_result = gmaps.geocode(city)
        if geocode_result:
            latitude = geocode_result[0]['geometry']['location']['lat']
            longitude = geocode_result[0]['geometry']['location']['lng']
            marker_locations.append(
                {'city': city, 'latitude': latitude, 'longitude': longitude})

    return render_template('users/map.html',  marker_locations=marker_locations)


@app.route('/analytics')
def plot():
    # # Render the template with the plot data
    # , plot_html=plot_html, plot_timeline=plot_timeline)
    return render_template('users/analytics.html')
