from flask import (
    Blueprint,
    render_template,
    request,
    jsonify
)

from services.ai_service import CyberShieldAI

bp = Blueprint(
    "gate",
    __name__,
    url_prefix="/gate"
)


@bp.route("/")
def index():

    return render_template(
        "gate/index.html"
    )


@bp.route("/solve", methods=["POST"])
def solve():

    try:

        data = request.get_json() or {}

        question = data.get(
            "question",
            ""
        ).strip()

        subject = data.get(
            "subject",
            "Operating System"
        )

        level = data.get(
            "level",
            "Medium"
        )

        if not question:

            return jsonify({
                "success": False,
                "answer": "Please enter a question."
            })

        # =====================================
        # Difficulty Levels
        # =====================================

        if level == "Easy":

            level_instruction = """
Explain in very simple language.

Include:
- Definition
- Simple Example
- Key Points

Maximum 150 words.
"""

        elif level == "Medium":

            level_instruction = """
Explain in exam-oriented language.

Include:
- Definition
- Explanation
- Important Points
- Formula if required

Maximum 350 words.
"""

        elif level == "GATE PYQ Level":

            level_instruction = """
Explain like a top GATE Faculty.

Include:

1. Definition
2. Detailed Theory
3. Formula
4. Diagram Explanation
5. Important Concepts
6. Shortcut Tricks
7. Common Mistakes
8. Previous Year Question Pattern
9. Interview Perspective

Minimum 500 words.
"""

        else:

            level_instruction = """
Give standard explanation.
"""

        prompt = f"""
You are an expert GATE Computer Science faculty.

Subject:
{subject}

Question:
{question}

Difficulty Level:
{level}

{level_instruction}

Generate response in clean HTML-friendly format.

Rules:

- Do NOT use **
- Do NOT use ###
- Do NOT use ---
- Do NOT use markdown

Use only:

Definition:

Explanation:

Important Points:

Formula:

IMPORTANT:

Do NOT generate markdown tables.

Do NOT use:

|
---
***

Use bullet points instead.

Example:

Normalization Types:

• 1NF
    - Each cell contains single value

• 2NF
    - Remove partial dependency

• 3NF
    - Remove transitive dependency

GATE Tip:

PYQ Insight:

At the end of every answer include:

PYQ Example:

Year:
Question:

Answer:

If real PYQ is unavailable,
generate a GATE-style PYQ.

Keep formatting clean.

Make answer complete and detailed.
Do not stop in middle.
"""

        answer = CyberShieldAI.ask(
            prompt
        )

        return jsonify({
            "success": True,
            "subject": subject,
            "level": level,
            "answer": answer
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "answer": f"Error: {str(e)}"
        })