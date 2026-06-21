from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from models import db
from models.course import Course, CourseProgress
from models.lesson import Lesson
from services.ai_service import CyberShieldAI
from flask import jsonify, request

from services.ai_tutor import AITutor

bp = Blueprint(
    "course",
    __name__,
    url_prefix="/course"
)


@bp.route("/")
@login_required
def list_courses():

    courses = Course.query.all()

    print("\n========== FLASK COURSES ==========")

    for c in courses:
        print(
            "ID =", c.id,
            "| TITLE =", c.title,
            "| PUBLISHED =", c.is_published
        )

    print("TOTAL =", len(courses))
    print("===================================\n")

    return render_template(
        "courses/list.html",
        courses=courses
    )

@bp.route("/<int:course_id>")
@login_required
def view_course(course_id):

    course = Course.query.get_or_404(course_id)

    progress = CourseProgress.query.filter_by(
        user_id=current_user.id,
        course_id=course.id
    ).first()

    if not progress:
        progress = CourseProgress(
            user_id=current_user.id,
            course_id=course.id,
            total_lessons=course.lessons_count
        )

        db.session.add(progress)
        db.session.commit()

    return render_template(
        "courses/view.html",
        course=course,
        progress=progress
    )


@bp.route("/<int:course_id>/complete")
@login_required
def complete_course(course_id):

    progress = CourseProgress.query.filter_by(
        user_id=current_user.id,
        course_id=course_id
    ).first()

    if progress:
        progress.mark_completed()
        db.session.commit()

        flash(
            "Course Completed Successfully!",
            "success"
        )

    return redirect(
        url_for("course.list_courses")
    )

@bp.route("/lesson/<int:lesson_id>")
@login_required
def lesson_view(lesson_id):

    lesson = Lesson.query.get_or_404(
        lesson_id
    )

    return render_template(
        "courses/lesson.html",
        lesson=lesson
    )

@bp.route("/ai-explain", methods=["POST"])
@login_required
def ai_explain():

    data = request.get_json()

    topic = data.get(
        "topic",
        ""
    )

    answer = AITutor.explain(
        topic
    )

    return jsonify({
        "answer": answer
    })

    data = request.get_json()

    topic = data.get("topic")

    prompt = f"""
    Explain {topic}
    for a cybersecurity beginner.

    Give:
    1. Simple explanation
    2. Real world example
    3. Attack example
    4. Prevention tips
    """

    answer = CyberShieldAI.ask(prompt)

    return jsonify({
        "answer": answer
    })

@bp.route("/ai-quiz", methods=["POST"])
@login_required
def ai_quiz():

    topic = request.json.get("topic")

    prompt = f"""
    Create 5 cybersecurity MCQ questions
    about:

    {topic}

    Include answers.
    """

    answer = CyberShieldAI.ask(prompt)

    return jsonify({
        "quiz": answer
    })
