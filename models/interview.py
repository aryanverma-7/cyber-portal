from datetime import datetime
from models import db


class InterviewSession(db.Model):

    __tablename__ = "interview_sessions"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        nullable=False
    )

    role = db.Column(
        db.String(100)
    )

    total_questions = db.Column(
        db.Integer,
        default=0
    )

    average_score = db.Column(
        db.Float,
        default=0
    )

    communication_score = db.Column(
        db.Float,
        default=0
    )

    technical_score = db.Column(
        db.Float,
        default=0
    )

    confidence_score = db.Column(
        db.Float,
        default=0
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )