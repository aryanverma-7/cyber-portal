from datetime import datetime
from models import db


class Course(db.Model):

    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(150), nullable=False)

    description = db.Column(db.Text, nullable=False)

    level = db.Column(db.String(20), nullable=False)

    category = db.Column(db.String(50), nullable=False)

    thumbnail = db.Column(
        db.String(255),
        default="default_course.png"
    )

    duration_minutes = db.Column(
        db.Integer,
        default=30
    )

    lessons_count = db.Column(
        db.Integer,
        default=5
    )

    instructor_id = db.Column(
        db.Integer,
        nullable=True
    )

    is_published = db.Column(
        db.Boolean,
        default=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    progress = db.relationship(
        "CourseProgress",
        backref="course",
        lazy=True,
        cascade="all, delete-orphan"
    )

    lessons = db.relationship(
        "Lesson",
        backref="course",
        lazy=True,
        cascade="all, delete-orphan"
    )

    certificates = db.relationship(
    "Certificate",
    backref="course",
    lazy=True
    )


    def get_completion_rate(self):

        if not self.progress:
            return 0

        completed = sum(
            1 for p in self.progress
            if p.is_completed
        )

        return round(
            (completed / len(self.progress)) * 100,
            2
        )


class CourseProgress(db.Model):

    __tablename__ = "course_progress"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    course_id = db.Column(
        db.Integer,
        db.ForeignKey("courses.id"),
        nullable=False
    )

    current_lesson = db.Column(
        db.Integer,
        default=1
    )

    total_lessons = db.Column(
        db.Integer,
        default=5
    )

    is_completed = db.Column(
        db.Boolean,
        default=False
    )

    points = db.Column(
        db.Integer,
        default=0
    )

    started_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    completed_at = db.Column(
        db.DateTime,
        nullable=True
    )

    last_accessed = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def get_progress_percentage(self):

        if self.total_lessons == 0:
            return 0

        return round(
            (self.current_lesson / self.total_lessons) * 100,
            2
        )

    def mark_completed(self):

        self.is_completed = True
        self.completed_at = datetime.utcnow()
        self.points = 100