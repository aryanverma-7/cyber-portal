from flask import (
    Blueprint,
    render_template,
    request,
    jsonify
)

from flask_login import current_user

import os

from services.interview_ai import InterviewAI
from services.interview_score_ai import InterviewScoreAI
from services.resume_interview_ai import ResumeInterviewAI
from services.resume_pdf_reader import ResumePDFReader

from models.interview import InterviewSession
from models import db


bp = Blueprint(
    "interview",
    __name__,
    url_prefix="/interview"
)


# =====================================================
# Main Interview Page
# =====================================================

@bp.route("/")
def index():

    return render_template(
        "interview/index.html"
    )


# =====================================================
# Generate Interview Question
# =====================================================

@bp.route("/question", methods=["POST"])
def question():

    data = request.get_json() or {}

    role = data.get(
        "role",
        "Cyber Security Analyst"
    )

    question = InterviewAI.generate_question(
        role
    )

    return jsonify({
        "success": True,
        "question": question
    })


# =====================================================
# Evaluate Answer
# =====================================================

@bp.route("/evaluate", methods=["POST"])
def evaluate():

    data = request.get_json() or {}

    role = data.get(
        "role",
        ""
    )

    question = data.get(
        "question",
        ""
    )

    answer = data.get(
        "answer",
        ""
    )

    result = InterviewAI.evaluate_answer(
        role,
        question,
        answer
    )

    try:

        if current_user.is_authenticated:

            session = InterviewSession(

                user_id=current_user.id,

                role=role,

                total_questions=1,

                average_score=0,

                communication_score=0,

                technical_score=0,

                confidence_score=0
            )

            db.session.add(session)
            db.session.commit()

    except Exception as e:

        print(
            "Interview Save Error:",
            e
        )

    return jsonify({
        "success": True,
        "result": result
    })


# =====================================================
# Resume Based Question
# =====================================================

@bp.route("/resume-question", methods=["POST"])
def resume_question():

    data = request.get_json() or {}

    resume_text = data.get(
        "resume_text",
        ""
    )

    question = (
        ResumeInterviewAI
        .generate_resume_question(
            resume_text
        )
    )

    return jsonify({
        "success": True,
        "question": question
    })


# =====================================================
# Final Score
# =====================================================

@bp.route("/final-score", methods=["POST"])
def final_score():

    data = request.get_json() or {}

    question = data.get(
        "question",
        ""
    )

    answer = data.get(
        "answer",
        ""
    )

    result = InterviewScoreAI.calculate(
        question,
        answer
    )

    return jsonify({
        "success": True,
        "result": result
    })


# =====================================================
# Next Question
# =====================================================

@bp.route("/next-question", methods=["POST"])
def next_question():

    data = request.get_json() or {}

    role = data.get(
        "role",
        "Cyber Security Analyst"
    )

    question = InterviewAI.generate_question(
        role
    )

    return jsonify({
        "success": True,
        "question": question
    })


# =====================================================
# Interview History
# =====================================================

@bp.route("/history")
def history():

    interviews = (
        InterviewSession
        .query
        .order_by(
            InterviewSession.created_at.desc()
        )
        .all()
    )

    return render_template(
        "interview/history.html",
        interviews=interviews
    )


# =====================================================
# Upload Resume PDF
# =====================================================

@bp.route("/upload-resume", methods=["POST"])
def upload_resume():

    try:

        if "resume" not in request.files:

            return jsonify({
                "success": False,
                "message": "No file uploaded"
            })

        file = request.files["resume"]

        if file.filename == "":

            return jsonify({
                "success": False,
                "message": "No file selected"
            })

        upload_folder = "uploads"

        os.makedirs(
            upload_folder,
            exist_ok=True
        )

        filepath = os.path.join(
            upload_folder,
            file.filename
        )

        file.save(
            filepath
        )

        resume_text = (
            ResumePDFReader
            .extract_text(
                filepath
            )
        )

        return jsonify({
            "success": True,
            "resume_text": resume_text
        })

    except Exception as e:

        print(
            "Resume Upload Error:",
            e
        )

        return jsonify({
            "success": False,
            "message": str(e)
        })