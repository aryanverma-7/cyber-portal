from flask import (
    Blueprint,
    render_template,
    request,
    jsonify
)

from flask_login import login_required
import os

from services.resume_pdf_ats import ResumePDFATS

bp = Blueprint(
    "resume",
    __name__,
    url_prefix="/resume"
)


@bp.route("/")
@login_required
def index():

    return render_template(
        "resume/index.html"
    )


@bp.route("/upload-pdf", methods=["POST"])
@login_required
def upload_pdf():

    if "resume" not in request.files:

        return jsonify({
            "success": False,
            "message": "No PDF Uploaded"
        })

    file = request.files["resume"]

    os.makedirs(
        "uploads",
        exist_ok=True
    )

    filepath = os.path.join(
        "uploads",
        file.filename
    )

    file.save(filepath)

    resume_text = ResumePDFATS.extract_text(
        filepath
    )

    return jsonify({
        "success": True,
        "resume_text": resume_text
    })


@bp.route("/analyze", methods=["POST"])
@login_required
def analyze_resume():

    data = request.get_json()

    resume_text = data.get(
        "resume",
        ""
    ).lower()

    skills_database = [

        "python",
        "flask",
        "django",
        "sql",
        "mysql",
        "mongodb",
        "html",
        "css",
        "javascript",
        "react",
        "networking",
        "cybersecurity",
        "linux",
        "git",
        "docker",
        "aws"
    ]

    found_skills = []

    for skill in skills_database:

        if skill in resume_text:

            found_skills.append(
                skill
            )

    required_skills = [

        "python",
        "sql",
        "linux",
        "git",
        "networking",
        "cybersecurity"
    ]

    missing_skills = []

    for skill in required_skills:

        if skill not in found_skills:

            missing_skills.append(
                skill
            )

    score = 0

    score += min(
        len(found_skills) * 5,
        30
    )

    if "project" in resume_text:
        score += 20

    if "internship" in resume_text:
        score += 15

    if (
        "certification" in resume_text
        or
        "certificate" in resume_text
    ):
        score += 10

    if "github" in resume_text:
        score += 10

    if "linkedin" in resume_text:
        score += 5

    education_keywords = [

        "btech",
        "b.tech",
        "bachelor",
        "degree",
        "college",
        "university"
    ]

    if any(
        word in resume_text
        for word in education_keywords
    ):
        score += 5

    if (
        "@" in resume_text
        or
        "phone" in resume_text
        or
        "mobile" in resume_text
    ):
        score += 5

    score = min(score, 100)

    suggestions = []

    if "github" not in resume_text:

        suggestions.append(
            "Add GitHub Profile"
        )

    if "project" not in resume_text:

        suggestions.append(
            "Add Projects Section"
        )

    if "internship" not in resume_text:

        suggestions.append(
            "Add Internship Experience"
        )

    if (
        "certification" not in resume_text
        and
        "certificate" not in resume_text
    ):

        suggestions.append(
            "Add Certifications"
        )

    if score >= 85:

        level = "Excellent"

    elif score >= 70:

        level = "Good"

    elif score >= 50:

        level = "Average"

    else:

        level = "Needs Improvement"

    return jsonify({

        "success": True,

        "score": score,

        "level": level,

        "skills": found_skills,

        "missing_skills": missing_skills,

        "suggestions": suggestions
    })