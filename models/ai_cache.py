from models import db

class AICache(db.Model):

    __tablename__ = "ai_cache"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    question = db.Column(
        db.Text,
        
        nullable=False
    )

    answer = db.Column(
        db.Text,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )