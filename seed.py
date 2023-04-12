from models import db, User, Job, Company, Contact, Document
from app import app
import random
from faker import Faker

fake = Faker()

with app.app_context():
    # Create all tables
    db.drop_all()
    db.create_all()

    users = []
    jobs = []
    companies = []
    contacts = []
    documents = []

    for i in range(5):
        first_name = fake.first_name()
        last_name = fake.last_name()
        username = f"{first_name.lower()}.{last_name.lower()}"
        email = f"{first_name.lower()}.{last_name.lower()}@example.com"
        password = "password"
        linkedin_url = fake.url()
        user_location = fake.city()

        user = User.signup(first_name, last_name, username, email,
                           password, linkedin_url, user_location)
        users.append(user)

    for i in range(5):
        company_name = fake.company()
        company_location = fake.city()
        company_url = fake.url()
        company_about = fake.text()

        company = Company(company_name=company_name, company_location=company_location,
                          company_url=company_url, company_about=company_about)
        companies.append(company)

    for i in range(5):
        user = random.choice(users)
        company = random.choice(companies)
        job_title = fake.job()
        post_url = fake.url()
        application_date = fake.date_between(
            start_date='-1y', end_date='today')
        status = random.choice(
            ['Applied', 'Phone Interview', 'On Site Interview', 'Offer', 'Rejected'])
        notes = fake.text()
        job_location = fake.city()
        job_description = fake.text()

        job = Job(user_id=user.id, company_id=company.id, job_title=job_title, post_url=post_url, application_date=application_date,
                  status=status, notes=notes, job_location=job_location, job_description=job_description)
        jobs.append(job)

    for i in range(5):
        user = random.choice(users)
        company = random.choice(companies)
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.email()
        phone = fake.phone_number()
        notes = fake.text()

        contact = Contact(user_id=user.id, company_id=company.id, first_name=first_name,
                          last_name=last_name, email=email, phone=phone, notes=notes)
        contacts.append(contact)

    for i in range(5):
        user = random.choice(users)
        job = random.choice(jobs)
        title = fake.text(max_nb_chars=50)
        category = random.choice(
            ['Cover Letter', 'Resume', 'Transcript', 'Certificate'])
        file_url = fake.file_path()

        document = Document(user_id=user.id, job_id=job.id,
                            title=title, category=category, file_url=file_url)
        documents.append(document)

    db.session.add_all(users)
    db.session.add_all(companies)
    db.session.add_all(jobs)
    db.session.add_all(contacts)
    db.session.add_all(documents)
    db.session.commit()
