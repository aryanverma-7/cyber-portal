import os
from datetime import timedelta

class Config:
    """Main configuration class for CyberShield"""
    
    # Base paths
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    TEMPLATE_FOLDER = os.path.join(BASE_DIR, 'templates')
    STATIC_FOLDER = os.path.join(BASE_DIR, 'static')
    REPORTS_DIR = os.path.join(BASE_DIR, 'reports')
    CERTIFICATES_DIR = os.path.join(BASE_DIR, 'certificates')
    UPLOADS_DIR = os.path.join(BASE_DIR, 'uploads')
    LOGS_DIR = os.path.join(BASE_DIR, 'logs')
    
    # Database configuration
    MYSQL_USER = os.getenv('MYSQL_USER', 'cybershield_user')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'CyberShield2024!Secure')
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'cybershield')
    
    SQLALCHEMY_DATABASE_URI = (
    "mysql+pymysql://cybershield_user:"
    "CyberShield2024!Secure@localhost/cybershield"
)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    
    # Security
    SECRET_KEY = os.getenv('SECRET_KEY', 'CyberShield-Secret-Key-2024-Secure-Platform')
    SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT', 'CyberShieldSalt2024')
    
    # Session configuration
    SESSION_TYPE = 'sqlalchemy'
    SESSION_PERMANENT = True
    SESSION_TIMEOUT = timedelta(hours=24)
    SESSION_COOKIE_NAME = 'cybershield_session'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Flask-WTF
    WTF_CSRF_ENABLED = False
    WTF_CSRF_TIME_LIMIT = 3600  # 1 hour
    
    # File uploads
    MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_UPLOAD_EXTENSIONS = ['pdf', 'png', 'jpg', 'jpeg', 'gif']
    
    # Email configuration (for password reset)
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', '')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', '')
    
    # AI Chatbot configuration
    CHATBOT_MAX_TOKENS = 500
    CHATBOT_TEMPERATURE = 0.7
    
    # CTF configuration
    CTF_CHALLENGE_TIMEOUT = 172800  # 48 hours
    CTF_MAX_SUBMISSIONS = 10
    
    # Rate limiting
    RATE_LIMIT_REQUESTS = 100
    RATE_LIMIT_WINDOW = 60  # seconds
    
    # Logging
    LOG_LEVEL = 'INFO'
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'