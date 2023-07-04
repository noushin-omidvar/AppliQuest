from models import db, User, Job, Company, Contact, Document, Task
from app import app
import random
from faker import Faker
from faker_file.providers.pdf_file import PdfFileProvider

import requests
import random

url = "https://api.openaq.org/v1/locations"

params = {
    "country": "US",
    "limit": 10000
}

response = requests.get(url, params=params)

# Get the JSON data from the response
data = response.json()


# Create a Faker object to generate fake data

fake = Faker()
fake.add_provider(PdfFileProvider)

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
    for i in range(3):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = f"{first_name.lower()}.{last_name.lower()}@example.com"
        password = "password"
        linkedin_url = f"https://www.linkedin.com/in/{first_name}-{last_name}"

        user_location = random.choice(data['results'])['city']

        # Create a new User object with the fake data and add it to the list
        user = User.signup(first_name, last_name, email,
                           password, linkedin_url, user_location)
        db.session.add(user)
        users.append(user)
    db.session.commit()

    # Generate five fake company profiles
    for i in range(50):

        company_name = fake.company()

        company_location = random.choice(data['results'])['city']

        company_url = fake.url()
        company_about = fake.text()

        # Create a new Company object with the fake data and add it to the list
        company = Company(company_name=company_name, company_location=company_location,
                          company_url=company_url, company_about=company_about)
        db.session.add(company)
        companies.append(company)
    db.session.commit()

    # Generate five fake job postings and associate them with users and companies
    for i in range(50):
        user = random.choice(users)
        company = random.choice(companies)
        job_title = fake.job()
        post_url = fake.url()
        application_date = fake.date_between(
            start_date='-1y', end_date='today')
        status = random.choice(
            ['Wishlist', 'Applied', 'Interview', 'Offer', 'Rejected'])
        notes = fake.text()

        job_location = random.choice(data['results'])['city']

        job_description = fake.text()
        created_at = fake.date_between(start_date='-1y', end_date='today')
        # Create a new Job object with the fake data and add it to the list
        job = Job(user_id=user.id, company_id=company.id, job_title=job_title, post_url=post_url, application_date=application_date,
                  status=status, notes=notes, job_location=job_location, job_description=job_description, created_at=created_at)
        db.session.add(job)
        jobs.append(job)
    db.session.commit()

    # Generate five fake contacts and associate them with users and companies
    for i in range(50):
        user = random.choice(users)
        company = random.choice(companies)
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = first_name+'.'+last_name +'@example.com'
        phone = fake.phone_number()
        notes = fake.text()

        # Create a new Contact object with the fake data and add it to the list
        contact = Contact(user_id=user.id, company_id=company.id, first_name=first_name,
                          last_name=last_name, email=email, phone=phone, notes=notes)
        db.session.add(contact)
        contacts.append(contact)
    db.session.commit()

    # # Generate five fake documents and associate them with users and jobs
    # for i in range(5):
    #     user = random.choice(users)
    #     job = random.choice(jobs)
    #     title = fake.text(max_nb_chars=20)
    #     category = random.choice(
    #         ['Cover Letter', 'Resume', 'Transcript', 'Certificate'])
    #     TEMPLATE = """
    #         {{name}}
    #         {{address}}
    #         {{phone_number}}

    #         {{text}} {{text}} {{text}}

    #         {{text}} {{text}} {{text}}

    #         {{text}} {{text}} {{text}}
            
    #         """



    #     file = fake.pdf_file(
    #         content=TEMPLATE, wrap_chars_after=80).encode('utf-8')

    #     document = Document(user_id=user.id,
    #                         title=title, category=category, file=file)
    #     db.session.add(document)
    #     documents.append(document)

    # db.session.commit()

    # Generate five fake tasks and associate them with users and jobs
    for i in range(50):
        user = random.choice(users)
        job = random.choice(jobs)
        task_title = fake.text(max_nb_chars=20)
        task = fake.text(max_nb_chars=200)
        completed = random.choice([True, False])
        notes = fake.text()
        task = Task(user_id=user.id, job_id=job.id,
                    task=task, task_title=task_title, completed=completed, notes=notes)
        db.session.add(task)
        documents.append(task)

    db.session.commit()
