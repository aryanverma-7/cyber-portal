from models import db


class Lesson(db.Model):

    __tablename__ = "lessons"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    course_id = db.Column(
        db.Integer,
        db.ForeignKey("courses.id"),
        nullable=False
    )

    title = db.Column(
        db.String(255),
        nullable=False
    )

    content = db.Column(
        db.Text
    )

    video_url = db.Column(
        db.String(500)
    )

    resource_url = db.Column(
        db.String(500)
    )