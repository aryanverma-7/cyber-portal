from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import bcrypt

from models import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(20), default='student')  # student, instructor, admin
    avatar = db.Column(db.String(255), default='default_avatar.png')
    bio = db.Column(db.Text, nullable=True)
    organization = db.Column(db.String(150), nullable=True)
    country = db.Column(db.String(50), default='India')
    is_active = db.Column(db.Boolean, default=True)
    is_email_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    password_reset_token = db.Column(db.String(255), nullable=True)
    password_reset_expires = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    course_progress = db.relationship('CourseProgress', backref='user', lazy='dynamic')
    quiz_scores = db.relationship('QuizScore', backref='user', lazy='dynamic')
    certificates = db.relationship('Certificate', backref='user', lazy='dynamic')
    reports = db.relationship('Report', backref='user', lazy='dynamic')
    phishing_cases = db.relationship('PhishingCase', backref='user', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_avatar_url(self):
        if self.avatar and self.avatar != 'default_avatar.png':
            return f'/static/images/{self.avatar}'
        return '/static/images/default_avatar.png'
    
    def get_role_icon(self):
        role_icons = {
            'student': '👨‍🎓',
            'instructor': '👩‍🏫',
            'admin': '🛡️'
        }
        return role_icons.get(self.role, '👤')
    
    def get_total_points(self):
        course_points = sum(
            cp.points for cp in self.course_progress.all()
            if hasattr(cp, "points")
        )

        quiz_points = sum(
        qs.points for qs in self.quiz_scores.all()
        if hasattr(qs, "points")
        )
        return course_points + quiz_points
    
    def is_instructor(self):
        return self.role in ['instructor', 'admin']
    
    def is_admin(self):
        return self.role == 'admin'