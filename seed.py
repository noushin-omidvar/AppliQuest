from models import db, User, Job, Company, Contact, Document, Task
from app import app
import random
from faker import Faker

# Create a Faker object to generate fake data

fake = Faker()

with app.app_context():

    # Drop all existing tables and create new ones
    db.drop_all()
    db.create_all()

    # Create empty lists to hold the objects we'll be adding to the database
    users = []
    jobs = []
    companies = []
    contacts = []
    documents = []

    # Generate five fake user profiles
    for i in range(5):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = f"{first_name.lower()}.{last_name.lower()}@example.com"
        password = "password"
        linkedin_url = f"https://www.linkedin.com/in/{first_name}-{last_name}"
        user_location = fake.city()

        # Create a new User object with the fake data and add it to the list
        user = User.signup(first_name, last_name, email,
                           password, linkedin_url, user_location)
        db.session.add(user)
        users.append(user)
    db.session.commit()

    # Generate five fake company profiles
    for i in range(5):

        company_name = fake.company()
        company_location = fake.city()
        company_url = fake.url()
        company_about = fake.text()

        # Create a new Company object with the fake data and add it to the list
        company = Company(company_name=company_name, company_location=company_location,
                          company_url=company_url, company_about=company_about)
        db.session.add(company)
        companies.append(company)
    db.session.commit()

    # Generate five fake job postings and associate them with users and companies
    for i in range(5):
        user = random.choice(users)
        company = random.choice(companies)
        job_title = fake.job()
        post_url = fake.url()
        application_date = fake.date_between(
            start_date='-1y', end_date='today')
        status = random.choice(
            ['Wishlist', 'Applied', 'Interview', 'Offer', 'Rejected'])
        notes = fake.text()
        job_location = fake.city()
        job_description = fake.text()
        # Create a new Job object with the fake data and add it to the list
        job = Job(user_id=user.id, company_id=company.id, job_title=job_title, post_url=post_url, application_date=application_date,
                  status=status, notes=notes, job_location=job_location, job_description=job_description)
        db.session.add(job)
        jobs.append(job)
    db.session.commit()

    # Generate five fake contacts and associate them with users and companies
    for i in range(5):
        user = random.choice(users)
        company = random.choice(companies)
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.email()
        phone = fake.phone_number()
        notes = fake.text()

        # Create a new Contact object with the fake data and add it to the list
        contact = Contact(user_id=user.id, company_id=company.id, first_name=first_name,
                          last_name=last_name, email=email, phone=phone, notes=notes)
        db.session.add(contact)
        contacts.append(contact)
    db.session.commit()

    # Generate five fake documents and associate them with users and jobs
    for i in range(5):
        user = random.choice(users)
        job = random.choice(jobs)
        title = fake.text(max_nb_chars=50)
        category = random.choice(
            ['Cover Letter', 'Resume', 'Transcript', 'Certificate'])
        file_url = fake.file_path()

        document = Document(user_id=user.id, job_id=job.id,
                            title=title, category=category, file_url=file_url)
        db.session.add(document)
        documents.append(document)

    db.session.commit()

    # Generate five fake tasks and associate them with users and jobs
    for i in range(5):
        user = random.choice(users)
        job = random.choice(jobs)
        task = fake.text(max_nb_chars=50)
        completed = random.choice([True, False])
        notes = fake.text()
        task = Task(user_id=user.id, job_id=job.id,
                    task=task, completed=completed, notes=notes)
        db.session.add(task)
        documents.append(task)

    db.session.commit()
