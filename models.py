import uuid
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.dialects.postgresql import UUID
from datetime import date


bcrypt = Bcrypt()
db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """ User table"""

    __tablename__ = "users"

    id = db.Column(UUID(as_uuid=True),
                   primary_key=True,
                   default=uuid.uuid4)

    first_name = db.Column(db.String,
                           nullable=False)

    last_name = db.Column(db.String,
                          nullable=False)

    email = db.Column(db.String,
                      nullable=False,
                      unique=True)

    password = db.Column(db.String,
                         nullable=False)

    linkedin_url = db.Column(db.String,
                             nullable=True)

    user_location = db.Column(db.String,
                              nullable=True)

    def __repr__(self):
        return f"<User #{self.id}: {self.first_name} {self.last_name}>"

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @classmethod
    def signup(cls, first_name, last_name, email, password, linkedin_url, user_location):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        # Create a new User object
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hashed_pwd,
            linkedin_url=linkedin_url,
            user_location=user_location
        )

        # Add the new user to the database
        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, email, password):
        """Find user with `email` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        # Search the database for a user with the given email
        user = cls.query.filter_by(email=email).first()

        # If such a user is found, check the password hash
        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        # If no user is found or the password hash doesn't match, return False
        return False


class Job(db.Model):
    """Aplication tabel"""

    __tablename__ = "jobs"

    id = db.Column(UUID(as_uuid=True),
                   primary_key=True,
                   default=uuid.uuid4)

    user_id = db.Column(UUID(as_uuid=True),
                        db.ForeignKey('users.id', ondelete="cascade"))

    company_id = db.Column(UUID(as_uuid=True),
                           db.ForeignKey('companies.id'))

    job_title = db.Column(db.String,
                          nullable=False)

    post_url = db.Column(db.String,
                         nullable=True)

    application_date = db.Column(db.Date,
                                 nullable=True,
                                 default=date.today())

    status = db.Column(db.String,
                       nullable=False
                       )

    notes = db.Column(db.Text,
                      nullable=True)

    job_location = db.Column(db.String,
                             nullable=True)

    job_description = db.Column(db.Text,
                                nullable=True)

    created_at = db.Column(
        db.Date,
        nullable=True,
        default=date.today(),
    )

    modified_at = db.Column(
        db.Date,
        nullable=True,
        default=date.today(),
    )

    user = db.relationship('User', backref='jobs')
    company = db.relationship('Company', backref="jobs")

    @classmethod
    def get_jobs_by_status(cls, user_id, status):
        """Retrieve jobs with status 'wishlist' for a specific user ID."""

        jobs = cls.query.filter_by(user_id=user_id, status=status).all()
        return jobs

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Company(db.Model):
    """ Company table """

    __tablename__ = "companies"
    id = db.Column(UUID(as_uuid=True),
                   primary_key=True,
                   default=uuid.uuid4)

    company_name = db.Column(db.String,
                             nullable=False)

    company_location = db.Column(db.String,
                                 nullable=True)

    company_url = db.Column(db.String,
                            nullable=True)

    company_about = db.Column(db.String,
                              nullable=True)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Contact(db.Model):
    """Contacts table"""

    __tablename__ = "contacts"

    id = db.Column(UUID(as_uuid=True),
                   primary_key=True,
                   default=uuid.uuid4)

    user_id = db.Column(UUID(as_uuid=True),
                        db.ForeignKey('users.id'))

    company_id = db.Column(UUID(as_uuid=True),
                           db.ForeignKey('companies.id'))

    first_name = db.Column(db.String,
                           nullable=False)

    last_name = db.Column(db.String,
                          nullable=False)

    email = db.Column(db.String,
                      nullable=True)

    phone = db.Column(db.String,
                      nullable=True)

    notes = db.Column(db.Text,
                      nullable=True)

    user = db.relationship('User', backref='contacts')
    company = db.relationship('Company', backref="contacts")

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Document(db.Model):
    """Documents Table"""

    __tablename__ = "documents"

    id = db.Column(UUID(as_uuid=True),
                   primary_key=True,
                   default=uuid.uuid4)

    user_id = db.Column(UUID(as_uuid=True),
                        db.ForeignKey('users.id'))

    title = db.Column(db.String,
                      nullable=False)

    category = db.Column(db.String,
                         nullable=False)

    file = db.Column(db.LargeBinary, nullable=False)

    created_at = db.Column(
        db.Date,
        nullable=True,
        default=date.today(),
    )

    user = db.relationship('User', backref='documents')

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Task(db.Model):
    """Tasks table"""

    __tablename__ = "tasks"

    id = db.Column(UUID(as_uuid=True),
                   primary_key=True,
                   default=uuid.uuid4)

    user_id = db.Column(UUID(as_uuid=True),
                        db.ForeignKey('users.id'))

    job_id = db.Column(UUID(as_uuid=True),
                       db.ForeignKey('jobs.id'),
                       nullable=True)

    task_title = db.Column(db.String(20),
                     nullable=False)
    
    task = db.Column(db.String,
                     nullable=False)

    completed = db.Column(db.Boolean,
                          nullable=True,
                          default=False)

    created_at = db.Column(
        db.Date,
        nullable=True,
        default=date.today(),
    )

    due_date = db.Column(db.Date,
                         nullable=True)

    notes = db.Column(db.Text,
                      nullable=True)

    user = db.relationship('User', backref='tasks')
    job = db.relationship('Job', backref="tasks")

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
