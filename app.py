from flask import Flask, render_template
from models import db, connect_db, User, Job, Company, Document, Task


app = Flask(__name__)
# Configuration
app.config.update(
    SQLALCHEMY_DATABASE_URI='postgresql:///appliquest',  # database URI
    SQLALCHEMY_TRACK_MODIFICATIONS=False,  # disable modification tracking
    SQLALCHEMY_ECHO=True,  # log SQL statements
    SECRET_KEY='ApPlIqUeSt',  # secret key for Flask sessions
    DEBUG_TB_INTERCEPT_REDIRECTS=False,  # disable debug toolbar redirects
)

# Database setup
connect_db(app)

with app.app_context():
    db.create_all()

# Define routes


@app.route('/')
def index():
    return render_template('index.html')
