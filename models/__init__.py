from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from models.user import User
from models.course import Course, CourseProgress
from models.quiz import QuizQuestion, QuizScore
from models.phishing import PhishingCase
from models.certificate import Certificate
from models.report import Report
from models.lesson import Lesson
from models.interview import InterviewSession
from models.ai_cache import AICache

__all__ = [
    'db',
    'User',
    'Course',
    'CourseProgress',
    'QuizQuestion',
    'QuizScore',
    'PhishingCase',
    'Certificate',
    'Report',
    'Lesson',
    'InterviewSession',
    'AICache'
]