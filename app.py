import os
import logging
from pathlib import Path

from flask import Flask, redirect, url_for, render_template
from flask_login import LoginManager
from flask_wtf import CSRFProtect

from config import Config
from models import db

# ==================================================
# Create Required Directories
# ==================================================

BASE_DIR = Path(__file__).resolve().parent

required_dirs = [
    BASE_DIR / "reports",
    BASE_DIR / "certificates",
    BASE_DIR / "uploads",
    BASE_DIR / "logs",
    BASE_DIR / "static",
    BASE_DIR / "static" / "css",
    BASE_DIR / "static" / "js",
    BASE_DIR / "static" / "images",
    BASE_DIR / "templates"
]

for folder in required_dirs:
    folder.mkdir(parents=True, exist_ok=True)

# ==================================================
# Flask App
# ==================================================

app = Flask(
    __name__,
    template_folder=Config.TEMPLATE_FOLDER,
    static_folder=Config.STATIC_FOLDER
)

app.config.from_object(Config)

# ==================================================
# Logging
# ==================================================

logging.basicConfig(
    level=logging.INFO,
    format=Config.LOG_FORMAT,
    handlers=[
        logging.FileHandler(
            os.path.join(Config.LOGS_DIR, "cybershield.log")
        ),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# ==================================================
# Extensions
# ==================================================

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth.login"
login_manager.login_message = "Please log in to continue."
login_manager.login_message_category = "info"

csrf = CSRFProtect(app)

# ==================================================
# Import Models
# ==================================================

from models.user import User
from models.course import Course, CourseProgress
from models.quiz import QuizQuestion, QuizScore
from models.phishing import PhishingCase
from models.certificate import Certificate
from models.report import Report
from models.lesson import Lesson
from models.interview import InterviewSession
from models.interview import InterviewSession


# ==================================================
# User Loader
# ==================================================

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# ==================================================
# Import Blueprints
# ==================================================

from routes.auth import bp as auth_bp
from routes.dashboard import bp as dashboard_bp
from routes.course import bp as course_bp
from routes.quiz import bp as quiz_bp
from routes.phishing import bp as phishing_bp
from routes.password import bp as password_bp
from routes.networking import bp as networking_bp
from routes.chatbot import bp as chatbot_bp
from routes.certificate import bp as certificate_bp
from routes.resume import bp as resume_bp
from routes.gate import bp as gate_bp
from routes.placement import bp as placement_bp
from routes.interview import bp as interview_bp 


# If report.py exists
try:
    from routes.report import bp as report_bp
    app.register_blueprint(report_bp)
except Exception as e:
    print("Report Blueprint Skipped:", e)

# ==================================================
# Register Blueprints
# ==================================================

app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(course_bp)
app.register_blueprint(quiz_bp)
app.register_blueprint(phishing_bp)
app.register_blueprint(password_bp)
app.register_blueprint(networking_bp)
app.register_blueprint(chatbot_bp)
app.register_blueprint(certificate_bp)
app.register_blueprint(resume_bp)
app.register_blueprint(gate_bp)
app.register_blueprint(placement_bp)
app.register_blueprint(interview_bp)
# ==================================================
# Main Routes
# ==================================================

@app.route("/")
def home():
    return redirect(url_for("dashboard.index"))

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")
# ==================================================
# Error Pages
# ==================================================

@app.errorhandler(404)
def page_not_found(error):
    return render_template("errors/404.html"), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template("errors/500.html"), 500

# ==================================================
# Database Initialization
# ==================================================

def seed_courses():
    from models.course import Course

    if Course.query.count() > 0:
        return

    courses = [
        Course(
            title="Phishing Awareness",
            description="Learn phishing attacks and prevention.",
            level="beginner",
            category="phishing",
            duration_minutes=30,
            lessons_count=5
        ),
        Course(
            title="Password Security",
            description="Learn strong password practices.",
            level="beginner",
            category="password",
            duration_minutes=40,
            lessons_count=6
        ),
        Course(
            title="Network Fundamentals",
            description="Learn TCP/IP, DNS and Routing.",
            level="beginner",
            category="network",
            duration_minutes=60,
            lessons_count=8
        ),
        Course(
            title="Linux Basics",
            description="Linux commands and security.",
            level="beginner",
            category="linux",
            duration_minutes=50,
            lessons_count=7
        ),
        Course(
            title="Web Security",
            description="XSS, SQL Injection and OWASP.",
            level="intermediate",
            category="web-security",
            duration_minutes=90,
            lessons_count=10
        )
    ]

    for course in courses:
        db.session.add(course)

    db.session.commit()

    print("Courses added successfully")


def init_db():
    with app.app_context():
        db.create_all()
        seed_courses()
        logger.info("Database tables created successfully")

# ==================================================
# Debug Route Listing
# ==================================================

def print_routes():
    print("\n========== REGISTERED ROUTES ==========")

    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint} -> {rule}")

    print("=======================================\n")

# ==================================================
# Run Application
# ==================================================

if __name__ == "__main__":

    logger.info("Starting CyberShield Platform...")

    init_db()

    print_routes()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )