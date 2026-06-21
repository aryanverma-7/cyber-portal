from config import Config
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Table,
    TableStyle,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from datetime import datetime
from models.course import CourseProgress
from models.quiz import QuizScore
import os
import uuid


class ReportGenerator:
    """PDF Report Generator"""

    def __init__(self):
        self.reports_dir = Config.REPORTS_DIR

        # Create reports folder if it doesn't exist
        os.makedirs(self.reports_dir, exist_ok=True)

    def generate_progress_report(self, user):
        """Generate user progress report"""

        filename = f"progress_report_{user.id}_{uuid.uuid4().hex}.pdf"
        filepath = os.path.join(self.reports_dir, filename)

        # Use filepath, not filename
        doc = SimpleDocTemplate(filepath, pagesize=letter)

        styles = getSampleStyleSheet()
        content = []

        # Header
        content.append(
            Paragraph(
                "CYBERSHIELD - PROGRESS REPORT",
                styles["Title"]
            )
        )
        content.append(Spacer(1, 12))

        # User Information
        user_info = [
            ["Name", user.get_full_name()],
            ["Username", user.username],
            ["Email", user.email],
            ["Role", user.role],
            ["Organization", user.organization or "Not specified"],
            ["Report Date", datetime.utcnow().strftime("%B %d, %Y")]
        ]

        user_table = Table(user_info, colWidths=[120, 300])

        user_table.setStyle(
            TableStyle([
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
            ])
        )

        content.append(user_table)
        content.append(Spacer(1, 20))

        # Course Progress
        courses = CourseProgress.query.filter_by(
            user_id=user.id
        ).all()

        completed = sum(1 for c in courses if c.is_completed)
        total = len(courses)

        course_stats = [
            ["Total Courses", total],
            ["Completed", completed],
            ["In Progress", total - completed],
            [
                "Completion Rate",
                f"{(completed / total * 100) if total > 0 else 0:.1f}%"
            ]
        ]

        content.append(
            Paragraph("Course Progress", styles["Heading2"])
        )

        course_table = Table(course_stats)

        course_table.setStyle(
            TableStyle([
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
            ])
        )

        content.append(course_table)
        content.append(Spacer(1, 20))

        # Quiz Performance
        quizzes = QuizScore.query.filter_by(
            user_id=user.id
        ).all()

        correct = sum(1 for q in quizzes if q.is_correct)
        total_quizzes = len(quizzes)
        total_points = sum(q.points for q in quizzes)

        quiz_stats = [
            ["Total Quizzes", total_quizzes],
            ["Correct Answers", correct],
            [
                "Accuracy",
                f"{(correct / total_quizzes * 100) if total_quizzes > 0 else 0:.1f}%"
            ],
            ["Total Points", total_points]
        ]

        content.append(
            Paragraph("Quiz Performance", styles["Heading2"])
        )

        quiz_table = Table(quiz_stats)

        quiz_table.setStyle(
            TableStyle([
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
            ])
        )

        content.append(quiz_table)

        # Build PDF
        doc.build(content)

        return filename

    def generate_quiz_report(self, user):
        """Generate quiz report"""

        filename = f"quiz_report_{user.id}_{uuid.uuid4().hex}.pdf"
        filepath = os.path.join(self.reports_dir, filename)

        doc = SimpleDocTemplate(filepath, pagesize=letter)

        styles = getSampleStyleSheet()
        content = []

        content.append(
            Paragraph(
                "CYBERSHIELD - QUIZ REPORT",
                styles["Title"]
            )
        )

        content.append(Spacer(1, 20))

        quizzes = QuizScore.query.filter_by(
            user_id=user.id
        ).all()

        correct = sum(1 for q in quizzes if q.is_correct)
        total = len(quizzes)
        points = sum(q.points for q in quizzes)

        report_data = [
            ["Student", user.get_full_name()],
            ["Total Questions", total],
            ["Correct Answers", correct],
            ["Points Earned", points],
            [
                "Accuracy",
                f"{(correct / total * 100) if total > 0 else 0:.1f}%"
            ]
        ]

        table = Table(report_data)

        table.setStyle(
            TableStyle([
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
            ])
        )

        content.append(table)

        doc.build(content)

        return filename