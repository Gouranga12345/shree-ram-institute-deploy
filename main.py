
import os
from datetime import datetime

from dotenv import load_dotenv
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    jsonify,
)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError


# ==========================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv()

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv(
    "SECRET_KEY",
    "local-development-secret-key-change-before-deployment"
)

database_url = os.getenv("DATABASE_URL", "").strip()

if not database_url:
    raise RuntimeError(
        "DATABASE_URL is missing. Please configure it in your .env file."
    )


# ==========================================
# DATABASE URL CONFIGURATION
# ==========================================

# Support Neon PostgreSQL URLs for future deployment.

if database_url.startswith("postgres://"):
    database_url = database_url.replace(
        "postgres://",
        "postgresql+psycopg://",
        1
    )

elif database_url.startswith("postgresql://"):
    database_url = database_url.replace(
        "postgresql://",
        "postgresql+psycopg://",
        1
    )

app.config["SQLALCHEMY_DATABASE_URI"] = database_url

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_pre_ping": True
}

db = SQLAlchemy(app)


# ==========================================
# ADMISSION DATABASE MODEL
# ==========================================

class Admission(db.Model):

    __tablename__ = "admissions"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    full_name = db.Column(
        db.String(120),
        nullable=False
    )

    address = db.Column(
        db.Text,
        nullable=False
    )

    current_study = db.Column(
        db.String(60),
        nullable=False
    )

    course_interest = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(160),
        nullable=False
    )

    mobile = db.Column(
        db.String(20),
        nullable=False
    )

    message = db.Column(
        db.Text,
        nullable=True
    )

    batch = db.Column(
        db.String(20),
        nullable=False,
        default="2027"
    )

    submitted_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )


# ==========================================
# COURSES
# ==========================================

COURSES = [

    {
        "name": "DCA",
        "duration": "6–12 months",
        "level": "Foundation",
        "description": "Build confidence in computer fundamentals, office applications, internet use and everyday digital skills.",
        "tag": "Popular"
    },

    {
        "name": "PGDCA",
        "duration": "12 months",
        "level": "Advanced",
        "description": "Develop practical knowledge of programming, databases, operating systems and application development.",
        "tag": "Career focused"
    },

    {
        "name": "ADCA",
        "duration": "12 months",
        "level": "Professional",
        "description": "A practical pathway covering office productivity, accounting tools, internet applications and computer operations.",
        "tag": "Practical"
    },

    {
        "name": "Computer Fundamentals",
        "duration": "3 months",
        "level": "Beginner",
        "description": "Start from the basics: typing, Windows, file management, internet, email and safe computer use.",
        "tag": "Beginner friendly"
    },

    {
        "name": "Tally & Accounting",
        "duration": "3–6 months",
        "level": "Skill development",
        "description": "Learn computerised accounting concepts, business entries, GST concepts and reporting workflows.",
        "tag": "Job skill"
    },

    {
        "name": "Programming: C, C++ & Java",
        "duration": "Flexible",
        "level": "Programming",
        "description": "Understand programming logic, problem solving and the foundations of software development.",
        "tag": "Build skills"
    },

    {
        "name": "Python Programming",
        "duration": "Flexible",
        "level": "Programming",
        "description": "Learn Python fundamentals and progress towards practical scripts and beginner projects.",
        "tag": "In demand"
    },

    {
        "name": "Web Design & Development",
        "duration": "3–6 months",
        "level": "Project based",
        "description": "Create websites using HTML, CSS and JavaScript, with an introduction to responsive design.",
        "tag": "Create projects"
    },

    {
        "name": "MCA / Higher Studies Guidance",
        "duration": "As applicable",
        "level": "Guidance",
        "description": "Guidance for learners exploring MCA and other higher-study pathways. This is guidance, not a degree programme.",
        "tag": "Next step"
    },

]


# ==========================================
# ALUMNI PROFILES
# Replace sample details with approved details.
# ==========================================

ALUMNI = [

    {
        "name": "Ajit Kumar sahoo",
        "course": "PGDCA",
        "role": "Post Office India, BPM",
        "image": "static/images/student1.jpeg"
    },

    {
        "name": "Alumni Name 02",
        "course": "Computer Applications",
        "role": "Data Entry Operator,JIO",
        "image": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=500&auto=format&fit=crop"
    },

    {
        "name": "Alumni Name 03",
        "course": "Programming",
        "role": "Add current role or achievement",
        "image": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=500&auto=format&fit=crop"
    },

]


# ==========================================
# HOME PAGE
# ==========================================

@app.get("/")
def home():

    return render_template(
        "index.html",
        courses=COURSES,
        alumni=ALUMNI
    )


# ==========================================
# ADMISSION APPLICATION
# ==========================================

@app.post("/apply")
def apply():

    fields = [
        "full_name",
        "address",
        "current_study",
        "course_interest",
        "email",
        "mobile"
    ]

    data = {
        field: (request.form.get(field) or "").strip()
        for field in fields
    }

    # Validate required fields

    if not all(data.values()):

        flash(
            "Please complete all required fields before submitting.",
            "error"
        )

        return redirect(url_for("home") + "#apply")

    # Validate mobile number

    if len(data["mobile"]) < 10:

        flash(
            "Please enter a valid mobile number.",
            "error"
        )

        return redirect(url_for("home") + "#apply")

    # Create admission record

    admission = Admission(

        full_name=data["full_name"],

        address=data["address"],

        current_study=data["current_study"],

        course_interest=data["course_interest"],

        email=data["email"],

        mobile=data["mobile"],

        message=(request.form.get("message") or "").strip(),

        batch="2027"

    )

    try:

        db.session.add(admission)

        db.session.commit()

        flash(
            "Your application has been submitted successfully. The institute can contact you using the details provided.",
            "success"
        )

    except SQLAlchemyError:

        db.session.rollback()

        app.logger.exception(
            "Admission application could not be saved"
        )

        flash(
            "We could not save your application right now. Please try again later or contact the institute.",
            "error"
        )

    return redirect(url_for("home") + "#apply")


# ==========================================
# DATABASE HEALTH CHECK
# ==========================================

@app.get("/health")
def health():

    try:

        db.session.execute(text("SELECT 1"))

        return jsonify({
            "status": "ok",
            "database": "connected"
        })

    except SQLAlchemyError:

        db.session.rollback()

        app.logger.exception(
            "Database health check failed"
        )

        return jsonify({
            "status": "error",
            "database": "unavailable"
        }), 503


# ==========================================
# DATABASE INITIALIZATION COMMAND
# ==========================================

@app.cli.command("init-db")
def init_db():

    with app.app_context():

        db.create_all()

        print("Admission database table created successfully.")

        print(
            "Tables:",
            db.inspect(db.engine).get_table_names()
        )


# ==========================================
# APPLICATION STARTUP
# ==========================================

if __name__ == "__main__":

    with app.app_context():

        db.create_all()

        print("\n===================================")

        print("SHREE RAM INSTITUTE")

        print("DATABASE INITIALIZED")

        print(
            "DATABASE:",
            db.engine.url.render_as_string(
                hide_password=True
            )
        )

        print(
            "TABLES:",
            db.inspect(db.engine).get_table_names()
        )

        print("===================================\n")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=os.getenv(
            "FLASK_DEBUG",
            "false"
        ).lower() == "true"
    )
