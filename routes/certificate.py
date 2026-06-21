from flask import Blueprint
from flask import render_template

from flask_login import login_required
from flask_login import current_user

from datetime import datetime
import uuid

from models.course import Course

bp = Blueprint(
    "certificate",
    __name__,
    url_prefix="/certificate"
)


@bp.route("/generate/<int:course_id>")
@login_required
def generate(course_id):

    course = Course.query.get_or_404(
        course_id
    )

    certificate_code = str(
        uuid.uuid4()
    )[:8]

    return render_template(
        "certificate/view.html",
        username=current_user.username,
        course_name=course.title,
        date=datetime.now().strftime(
            "%d %B %Y"
        ),
        certificate_code=certificate_code
    )