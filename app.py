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


# Handling user data
# --------------------------------
@app.route('/api/users')
def list_users():
    """Get all users"""

    all_users = [u.as_dict() for u in User.query.all()]
    return jsonify(users=all_users)


@app.route('/api/users', methods=['POST'])
def create_user():
    """Create a new user"""

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


@app.route('/api/users/<user_id>')
def get_user(user_id):
    """get user by user_id"""

    user = User.query.get_or_404(user_id)
    return jsonify(user=user.to_dict())


@app.route('/api/users/<user_id>', methods=['PATCH'])
def update_user(user_id):
    """Update the user"""

    # Retrieve the user from the database
    user = User.query.get_404(user_id)

    if user is None:
        # Return a 404 error if the user is not found
        return jsonify({'error': 'User not found'}), 404

    db.session.query(User).filter(id=user_id).update(request.json)
    db.session.commit()

    # Return the updated user data
    return jsonify(user.to_dict())


@app.route('/api/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """DELETE the user"""

    # Retrieve the user from the database
    user = User.query.get_404(user_id)

    if user is None:
        # Return a 404 error if the user is not found
        return jsonify({'error': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()

    # Return the updated user data
    return jsonify(message="User deleted")


# Handling the jobs data
# ------------------------------

@app.route('/api/users/<user_id>/jobs', methods=['POST'])
def create_job():
    """Create a new job"""

    new_job = Job(user_id=request.json['user_id'],
                  company_id=request.json['company_id'],
                  job_title=request.json['job_title'],
                  post_url=request.json['post_url'],
                  application_date=request.json['application_date'],
                  status=request.json['status'],
                  notes=request.json['notes'],
                  job_location=request.json['job_location'],
                  job_description=request.json['job_description'],
                  )

    db.session.add(new_job)
    db.session.commit()
    return jsonify(new_job=new_job.to_dict())


@app.route('/api/users/<user_id>/jobs/<job_id>')
def get_job(user_id, job_id):
    """get job by job_id"""

    job = Job.query.get_or_404(job_id)
    return jsonify(job=job.to_dict())


@app.route('/api/users/<user_id>/jobs/<job_id>', methods=['PATCH'])
def update_job(user_id, job_id):
    """Update the job """

    job = Job.query.get(job_id)

    if job is None:
        return jsonify({'error': 'Job not found'}), 404

    db.session.query(Job).filter(
        id=job_id, user_id=user_id).update(request.json)
    db.session.commit()

    return jsonify(job.to_dict())


@app.route('/api/users/<user_id>/jobs/<job_id>', methods=['DELETE'])
def delete_job(job_id):
    """DELETE the job"""

    # Retrieve the user from the database
    job = Job.query.get_404(job_id)

    if job is None:
        # Return a 404 error if the job is not found
        return jsonify({'error': 'Job not found'}), 404

    db.session.delete(job)
    db.session.commit()

    # Return the updated job data
    return jsonify(message="job deleted")


# Handle contacts data
# -----------------------

@app.route('/api/users/<user_id>/contacts', methods=['POST'])
def create_contact():
    """Create a new contact"""

    new_contact = Contact(user_id=request.json['user_id'],
                          company_id=request.json['company_id'],
                          first_name=request.json['first_name'],
                          last_name=request.json['last_name'],
                          email=request.json['email'],
                          phone=request.json['phone'],
                          notes=request.json['notes'])

    db.session.add(new_contact)
    db.session.commit()
    return jsonify(new_contact=new_contact.to_dict())


@app.route('/api/users/<user_id>/contacts/<contact_id>')
def get_contact(user_id, contact_id):
    """get contact by contact_id"""

    contact = Contact.query.get_or_404(contact_id)
    return jsonify(contact=contact.to_dict())


@app.route('/api/users/<user_id>/contacts/<contact_id>', methods=['PATCH'])
def update_contact(user_id, contact_id):
    """ Update contact"""

    # Retrieve the contact from the database
    contact = Contact.query.get(contact_id)

    if contact is None:
        # Return a 404 error if the contact is not found
        return jsonify({'error': 'Contact not found'}), 404

    db.session.query(Contact).filter(id=contact_id).update(request.json)
    db.session.commit()

    # Return the updated contact data
    return jsonify(contact.to_dict())


@app.route('/api/users/<user_id>/contacts/<contact_id>', methods=['DELETE'])
def delete_contact(contact_id):
    """DELETE the contact"""

    # Retrieve the user from the database
    contact = Contact.query.get_404(contact_id)

    if contact is None:
        # Return a 404 error if the contact is not found
        return jsonify({'error': 'Contact not found'}), 404

    db.session.delete(contact)
    db.session.commit()

    # Return the updated contact data
    return jsonify(message="Contact deleted")


# Handling documents data
# -------------------------

@app.route('/api/users/<user_id>/documents', methods=['POST'])
def create_document():
    """Create a new document"""

    new_document = Document(user_id=request.json['user_id'],
                            job_id=request.json['job_id'],
                            title=request.json['title'],
                            category=request.json['category'],
                            file_url=request.json['file_url'])

    db.session.add(new_document)
    db.session.commit()
    return jsonify(new_document=new_document.to_dict())


@app.route('/api/users/<user_id>/documents/<document_id>')
def get_document(user_id, document_id):
    """get document by document_id"""

    document = Document.query.get_or_404(document_id)
    return jsonify(document=document.to_dict())


@app.route('/api/users/<user_id>/documents/<document_id>', methods=['PATCH'])
def update_document(user_id, document_id):
    # Retrieve the document from the database
    document = Document.query.get(document_id)

    if document is None:
        # Return a 404 error if the document is not found
        return jsonify({'error': 'Document not found'}), 404

    db.session.query(Document).filter(id=document_id).update(request.json)
    db.session.commit()

    # Return the updated document data
    return jsonify(document.to_dict())


@app.route('/api/users/<user_id>/documents/<document_id>', methods=['DELETE'])
def delete_document(document_id):
    """DELETE the contact"""

    # Retrieve the document from the database
    document = Document.query.get_404(document_id)

    if document is None:
        # Return a 404 error if the document is not found
        return jsonify({'error': 'Document not found'}), 404

    db.session.delete(document)
    db.session.commit()

    # Return the updated document data
    return jsonify(message="document deleted")


# Handling task data
# --------------------

@app.route('/api/users/<user_id>/tasks', methods=['POST'])
def create_task():
    """Create a new document"""

    new_task = Task(user_id=request.json['user_id'],
                    job_id=request.json['job_id'],
                    task=request.json['task'],
                    created_at=request.json['created_at'],
                    due_date=request.json['due_date'],
                    notes=request.json['notes'])

    db.session.add(new_task)
    db.session.commit()
    return jsonify(new_task=new_task.to_dict())


@app.route('/api/users/<user_id>/tasks/<task_id>')
def get_task(user_id, task_id):
    """get task by task_id"""

    task = Task.query.get_or_404(task_id)
    return jsonify(task=task.to_dict())


@app.route('/api/users/<user_id>/tasks/<task_id>', methods=['PATCH'])
def update_task(user_id, task_id):
    # Retrieve the task from the database
    task = Task.query.get(task_id)

    if task is None:
        # Return a 404 error if the task is not found
        return jsonify({'error': 'Task not found'}), 404

    db.session.query(Task).filter(id=task_id).update(request.json)
    db.session.commit()

    # Return the updated task data
    return jsonify(task.to_dict())


@app.route('/api/users/<user_id>/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    """DELETE the contact"""

    # Retrieve the document from the database
    task = Task.query.get_404(task_id)

    if task is None:
        # Return a 404 error if the document is not found
        return jsonify({'error': 'task not found'}), 404

    db.session.delete(task)
    db.session.commit()

    # Return the updated document data
    return jsonify(message="task deleted")


# Handle the companies data
# --------------------------

@app.route('/api/companiess/', methods=['POST'])
def create_company():
    """Create a new company"""

    new_company = Company(company_name=request.json['company_name'],
                          company_location=request.json['company_location'],
                          company_url=request.json['company_url'],
                          company_about=request.json['company_about'])

    db.session.add(new_company)
    db.session.commit()
    return jsonify(new_task=new_company.to_dict())


@app.route('/api/companies/<company_id>')
def get_task(user_id, company_id):
    """get company by company_id"""

    company = Company.query.get_or_404(company_id)
    return jsonify(company=company.to_dict())


@app.route('/api/companies/<company_id>', methods=['PATCH'])
def update_company(user_id, company_id):
    # Retrieve the company from the database
    company = Company.query.get(company_id)

    if company is None:
        # Return a 404 error if the company is not found
        return jsonify({'error': 'Company not found'}), 404

    db.session.query(Company).filter(id=company_id).update(request.json)
    db.session.commit()

    # Return the updated company data
    return jsonify(company.to_dict())


@app.route('/api/companies/<company_id>', methods=['DELETE'])
def delete_company(user_id, company_id):
    """DELETE the contact"""

    # Retrieve the document from the database
    company = Company.query.get_404(company_id)

    if company is None:
        # Return a 404 error if the company is not found
        return jsonify({'error': 'company not found'}), 404

    db.session.delete(company)
    db.session.commit()

    # Return the updated document data
    return jsonify(message="Company deleted")

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
