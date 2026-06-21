from datetime import datetime
from models import db
from config import Config

class Report(db.Model):
    __tablename__ = "reports"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    report_type = db.Column(db.String(100))
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    file_path = db.Column(db.String(255))

    generated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )