import uuid
import boto3
import botocore
import googlemaps
from datetime import date
from flask import Blueprint, session, jsonify, request
from models import db, User, Job, Company, Document, Task, Contact


CURR_USER_KEY = "curr_user"

api_bp = Blueprint('api/v1', __name__)

# --------------------
# Set up API endpoints
# --------------------


@api_bp.route('/user_id')
def user_id():
    # Get the user id from the session
    user_id = session.get(CURR_USER_KEY)
    # Return the user id as JSON
    return jsonify({'user_id': user_id})


# Handling user data
# --------------------------------
@api_bp.route('/users')
def list_users():
    """Get all users"""

    all_users = [u.as_dict() for u in User.query.all()]
    return jsonify(users=all_users)


@api_bp.route('/users', methods=['POST'])
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


@api_bp.route('/users/<user_id>')
def get_user(user_id):
    """get user by user_id"""

    user = User.query.get_or_404(user_id)
    return jsonify(user=user.to_dict())


@api_bp.route('/users/<user_id>', methods=['PATCH'])
def update_user(user_id):
    """Update the user"""

    # Retrieve the user from the database
    user = User.query.get_or_404(user_id)
    if user is None:
        # Return a 404 error if the user is not found
        return jsonify({'error': 'User not found'}), 404

    db.session.query(User).filter(id == user_id).update(request.json)
    db.session.commit()
    # Return the updated user data
    return jsonify(user.to_dict())


@api_bp.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """DELETE the user"""

    # Retrieve the user from the database
    user = User.query.get_or_404(user_id)

    if user is None:
        # Return a 404 error if the user is not found
        return jsonify({'error': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()

    # Return the updated user data
    return jsonify(message="User deleted")


# Handling the jobs data
# ------------------------------

@api_bp.route('/users/<user_id>/jobs', methods=['POST'])
def create_job(user_id):
    """Create a new job"""

    new_job = Job(user_id=user_id,
                  company_id=request.json['company']['id'],
                  job_title=request.json['job_title'],
                  post_url=request.json.get('post_url', None),
                  status=request.json.get('status', 'Wishlist'),
                  notes=request.json.get('notes', None),
                  job_location=request.json.get('job_location', None),
                  job_description=request.json.get('job_description', None),
                  )

    db.session.add(new_job)
    db.session.commit()
    return jsonify(new_job=new_job.to_dict())


@api_bp.route('/users/<user_id>/jobs')
def get_jobs(user_id):
    """get job by job_id"""

    jobs = [job.to_dict()
            for job in Job.query.filter(Job.user_id == user_id).all()]

    return jsonify(jobs=jobs)


@api_bp.route('/users/<user_id>/jobs/<job_id>')
def get_job(user_id, job_id):
    """get job by job_id"""

    job = Job.query.get_or_404(job_id)
    return jsonify(job=job.to_dict())


@api_bp.route('/users/<user_id>/jobs/<job_id>', methods=['PATCH'])
def update_job(user_id, job_id):
    """Update the job """
    job = Job.query.get(job_id)
    if job is None:
        return jsonify({'error': 'Job not found'}), 404

    db.session.query(Job).filter(
        Job.id == job_id).update(request.json)
    db.session.query(Job).filter(
        Job.id == job_id).update({'modified_at': date.today()})
    db.session.commit()

    return jsonify(job.to_dict())


@api_bp.route('/users/<user_id>/jobs/<job_id>', methods=['DELETE'])
def delete_job(user_id, job_id):
    """DELETE the job"""

    # Retrieve the user from the database
    job = Job.query.get_or_404(job_id)

    if job is None:
        # Return a 404 error if the job is not found
        return jsonify({'error': 'Job not found'}), 404

    db.session.delete(job)
    db.session.commit()

    # Return the updated job data
    return jsonify(message="job deleted")


# Handle contacts data
# -----------------------

@api_bp.route('/users/<user_id>/contacts', methods=['POST'])
def create_contact(user_id):
    """Create a new contact"""

    new_contact = Contact(user_id=user_id,
                          company_id=request.json['company_id'],
                          first_name=request.json['first_name'],
                          last_name=request.json['last_name'],
                          email=request.json['email'],
                          phone=request.json['phone'],
                          notes=request.json['notes'])

    db.session.add(new_contact)
    db.session.commit()
    return jsonify(new_contact=new_contact.to_dict())


@api_bp.route('/users/<user_id>/contacts/<contact_id>')
def get_contact(user_id, contact_id):
    """get contact by contact_id"""

    contact = Contact.query.get_or_404(contact_id)
    return jsonify(contact=contact.to_dict())


@api_bp.route('/users/<user_id>/contacts/<contact_id>', methods=['PATCH'])
def update_contact(user_id, contact_id):
    """ Update contact"""

    # Retrieve the contact from the database
    contact = Contact.query.get(contact_id)

    if contact is None:
        # Return a 404 error if the contact is not found
        return jsonify({'error': 'Contact not found'}), 404
    db.session.query(Contact).filter(Contact.id == contact_id,
                                     Contact.user_id == user_id).update(request.json)
    db.session.commit()

    # Return the updated contact data
    return jsonify(contact.to_dict())


@api_bp.route('/users/<user_id>/contacts/<contact_id>', methods=['DELETE'])
def delete_contact(contact_id, user_id):
    """DELETE the contact"""

    # Retrieve the user from the database
    contact = Contact.query.get_or_404(contact_id)

    if contact is None:
        # Return a 404 error if the contact is not found
        return jsonify({'error': 'Contact not found'}), 404

    db.session.delete(contact)
    db.session.commit()

    # Return the updated contact data
    return jsonify(message="Contact deleted")


# Handling documents data
# -------------------------

@api_bp.route('/users/<user_id>/documents', methods=['POST'])
def create_document(user_id):
    """Create a new document"""

    ALLOWED_EXTENSIONS = {'pdf'}

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    uploaded_file = request.files["file_to_save"]
    if not allowed_file(uploaded_file.filename):
        return "FILE NOT ALLOWED!"

    new_filename = uuid.uuid4().hex + '.' + \
        uploaded_file.filename.rsplit('.', 1)[1].lower()

    bucket_name = "appliquest"
    s3 = boto3.resource("s3")
    s3.Bucket(bucket_name).upload_fileobj(uploaded_file, new_filename,
                                          ExtraArgs={'ContentType': "application/pdf", 'Metadata': {'Content-Disposition': ''}})

    new_document = Document(user_id=user_id,
                            category=request.form.get('category'),
                            original_filename=uploaded_file.filename,
                            filename=new_filename,
                            bucket=bucket_name,)
    db.session.add(new_document)
    db.session.commit()

    return jsonify(new_document=new_document.to_dict())


@api_bp.route('/users/<user_id>/documents/<document_id>')
def get_document(user_id, document_id):
    """get document by document_id"""

    document = Document.query.get_or_404(document_id)
    return jsonify(document=document.to_dict())


@api_bp.route('/documents/<document_id>/file', methods=['GET'])
def get_document_file(document_id):
    document = Document.query.get(document_id)
    if not document:
        return "Document not found", 404

    s3 = boto3.client('s3')
    try:
        # Generate a presigned URL for accessing the photo in the S3 bucket
        presigned_url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': document.bucket, 'Key': document.filename},
            ExpiresIn=3600  # Set the URL expiration time as per your requirements
        )

        # Return the presigned URL to the browser
        return presigned_url
    except botocore.exceptions.ClientError as e:
        return "Failed to retrieve file from S3", 500


@api_bp.route('/users/<user_id>/documents/<document_id>', methods=['PATCH'])
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


@api_bp.route('/users/<user_id>/documents/<document_id>', methods=['DELETE'])
def delete_document(user_id, document_id):
    """DELETE the contact"""

    # Retrieve the document from the database
    document = Document.query.get_or_404(document_id)
    client = boto3.client('s3')

    if document is None:
        # Return a 404 error if the document is not found
        return jsonify({'error': 'Document not found'}), 404

    client.delete_object(Bucket='appliquest', Key=document.filename)

    db.session.delete(document)
    db.session.commit()

    # Return the updated document data
    return jsonify(message="document deleted")


# Handling task data
# --------------------

@api_bp.route('/users/<user_id>/tasks', methods=['POST'])
def create_task(user_id):
    """Create a new document"""

    new_task = Task(user_id=user_id,
                    job_id=request.json['job_id'],
                    task=request.json['task'],
                    created_at=request.json['startdate'],
                    due_date=request.json['enddate'],
                    notes=request.json['notes'])

    db.session.add(new_task)
    db.session.commit()
    return jsonify(new_task=new_task.to_dict())


@api_bp.route('/users/<user_id>/tasks/<task_id>')
def get_task(user_id, task_id):
    """get task by task_id"""

    task = Task.query.get_or_404(task_id)
    return jsonify(task=task.to_dict())


@api_bp.route('/users/<user_id>/tasks/<task_id>', methods=['PATCH'])
def update_task(user_id, task_id):
    # Retrieve the task from the database
    task = Task.query.get(task_id)
    if task is None:
        # Return a 404 error if the task is not found
        return jsonify({'error': 'Task not found'}), 404

    db.session.query(Task).filter(Task.id == task_id).update(request.json)
    db.session.commit()

    # Return the updated task data
    return jsonify(task.to_dict())


@api_bp.route('/users/<user_id>/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id, user_id):
    """DELETE the contact"""

    # Retrieve the document from the database
    task = Task.query.get_or_404(task_id)

    if task is None:
        # Return a 404 error if the document is not found
        return jsonify({'error': 'task not found'}), 404

    db.session.delete(task)
    db.session.commit()

    # Return the updated document data
    return jsonify(message="task deleted")


# Handle the companies data
# --------------------------

@api_bp.route('/companies/', methods=['POST'])
def create_company():
    """Create a new company"""

    new_company = Company(company_name=request.json.get('company_name', None),
                          company_location=request.json.get(
                              'company_location', None),
                          company_url=request.json.get('company_url', None),
                          company_about=request.json.get('company_about', None))

    db.session.add(new_company)
    db.session.commit()
    return jsonify(new_company=new_company.to_dict())


@api_bp.route('/companies/<company_id>')
def get_company(company_id):
    """get company by company_id"""

    company = Company.query.get_or_404(company_id)
    return jsonify(company=company.to_dict())


@api_bp.route('/companies/<company_id>', methods=['PATCH'])
def update_company(user_id, company_id):
    # Retrieve the company from the database
    company = Company.query.get(company_id)

    if company is None:
        # Return a 404 error if the company is not found
        return jsonify({'error': 'Company not found'}), 404

    db.session.query(Company).filter(id == company_id).update(request.json)
    db.session.commit()

    # Return the updated company data
    return jsonify(company.to_dict())


@api_bp.route('/companies/<company_id>', methods=['DELETE'])
def delete_company(user_id, company_id):
    """DELETE the company"""

    # Retrieve the document from the database
    company = Company.query.get_or_404(company_id)

    if company is None:
        # Return a 404 error if the company is not found
        return jsonify({'error': 'company not found'}), 404

    db.session.delete(company)
    db.session.commit()

    # Return the updated document data
    return jsonify(message="Company deleted")


@api_bp.route('/companies/autocomplete_company', methods=['POST'])
def autocomplete_company():
    query = request.json['query']
    companies = Company.query.filter(
        Company.company_name.ilike('%' + query + '%')).all()
    return jsonify([c.company_name for c in companies])


@api_bp.route('/companies')
def list_company():
    """get companies"""

    companies = [c.to_dict() for c in Company.query.all()]

    return jsonify(companies=companies)


@api_bp.route('/users/<user_id>/map', methods=['GET'])
def get_job_locations(user_id):
    user_jobs = Job.query.filter_by(user_id=user_id).all()
    job_locations = [job.job_location for job in user_jobs if job.job_location]
    locations = []
    for city in job_locations:
        gmaps = googlemaps.Client(api_key='YOUR_API_KEY')
        geocode_result = gmaps.geocode(city)
        if geocode_result:
            latitude = geocode_result[0]['geometry']['location']['lat']
            longitude = geocode_result[0]['geometry']['location']['lng']
            locations.append(
                {'city': city, 'latitude': latitude, 'longitude': longitude})
    return jsonify(locations)
