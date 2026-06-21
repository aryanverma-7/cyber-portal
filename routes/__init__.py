from routes.auth import bp as auth_bp
from routes.dashboard import bp as dashboard_bp
from routes.course import bp as course_bp
from routes.quiz import bp as quiz_bp
from routes.phishing import bp as phishing_bp
from routes.password import bp as password_bp
from routes.report import bp as report_bp
from routes.networking import bp as networking_bp
from routes.chatbot import bp as chatbot_bp

__all__ = [
    'auth_bp',
    'dashboard_bp',
    'course_bp',
    'quiz_bp',
    'phishing_bp',
    'password_bp',
    'report_bp',
    'networking_bp',
    'chatbot_bp'
]