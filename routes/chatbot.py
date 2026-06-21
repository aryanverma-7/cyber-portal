from flask import (
    Blueprint,
    render_template,
    request,
    jsonify
)

from flask_login import login_required

from services.ai_service import (
    CyberShieldAI
)

bp = Blueprint(
    "chatbot",
    __name__,
    url_prefix="/chatbot"
)


@bp.route("/")
@login_required
def index():

    return render_template(
        "chatbot/index.html"
    )


@bp.route("/ask", methods=["POST"])
@login_required
def ask():

    data = request.get_json()

    question = data.get(
        "question",
        ""
    )

    answer = CyberShieldAI.ask_html(
        question
    )

    return jsonify({
        "answer": answer
    })