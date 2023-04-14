import os

from flask import Flask, render_template, session, g, redirect, flash, jsonify, request
from flask_debugtoolbar import DebugToolbarExtension

from sqlalchemy.exc import IntegrityError

from models import db, connect_db, User, Job, Company, Document, Task, Contact

from forms import SignUpForm, LoginForm, AddJobForm

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///appliquest'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
toolbar = DebugToolbarExtension(app)

connect_db(app)

# --------------------
# Set up API endpoints
# --------------------


@app.route('/api/users')
def list_users():
    all_users = [u.as_dict() for u in User.query.all()]
    return jsonify(users=all_users)


@app.route('/api/users/<user_id>')
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user=user.to_dict())


@app.route('/api/users/<user_id>', methods=['POST'])
def create_user(user_id):

    new_user = User(first_name=request.json['first_name'],
                    last_name=request.json['last_name'],
                    email=request.json['email'],
                    password=request.json['password'],
                    linkedin_url=request.json['linkedin_url'],
                    user_location=request.json['user_location']
                    )

    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user=new_user.to_dict())


@app.route('/api/users/<user_id>', methods=['PATCH'])
def update_user(user_id):
    # Retrieve the user from the database
    user = User.query.get(user_id)

    if user is None:
        # Return a 404 error if the user is not found
        return jsonify({'error': 'User not found'}), 404

    db.session.query(User).filter(id=user_id).update(request.json)
    db.session.commit()

    # Return the updated user data
    return jsonify(user.to_dict())


@app.route('/api/users/<user_id>/jobs/<job_id>', methods=['PATCH'])
def update_job(user_id, job_id):
    # Retrieve the job from the database
    job = Job.query.get(job_id)

    if job is None:
        # Return a 404 error if the job is not found
        return jsonify({'error': 'Job not found'}), 404

    db.session.query(Job).filter(id=job_id).update(request.json)
    db.session.commit()

    # Return the updated job data
    return jsonify(job.to_dict())


@app.route('/api/users/<user_id>/contacts/<contact_id>', methods=['PATCH'])
def update_contact(user_id, contact_id)
  # Retrieve the contact from the database
  contact = Contact.query.get(contact_id)

   if contact is None:
        # Return a 404 error if the contact is not found
        return jsonify({'error': 'Contact not found'}), 404

    db.session.query(Contact).filter(id=contact_id).update(request.json)
    db.session.commit()

    # Return the updated contact data
    return jsonify(contact.to_dict())

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
            return render_template('/')

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
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('users/login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()
    flash("You have been loged out", "info")

    return redirect('/')

# Define general routes


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

    form = AddJobForm()
    jobs = Job.query.all()
    return render_template('users/board.html', jobs=jobs, form=form)


# with app.app_context():
#     u = User.query.first()
#     print(u.as_dict())
