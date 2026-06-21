from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request,
    jsonify
)

from flask_login import (
    login_required,
    current_user
)

from sqlalchemy import func

from models import db
from models.quiz import QuizQuestion, QuizScore
from models.user import User

from services.quiz_generator import generate_quiz
from services.ai_service import CyberShieldAI


bp = Blueprint(
    "quiz",
    __name__,
    url_prefix="/quiz"
)


# =====================================================
# Quiz List
# =====================================================

@bp.route("/")
@login_required
def list_quizzes():

    difficulty = request.args.get("difficulty", "")
    category = request.args.get("category", "")

    query = QuizQuestion.query.filter(
        QuizQuestion.is_active == True
    )

    if difficulty:
        query = query.filter(
            QuizQuestion.difficulty == difficulty
        )

    if category:
        query = query.filter(
            QuizQuestion.category == category
        )

    questions = query.all()

    difficulties = [
        "easy",
        "medium",
        "hard"
    ]

    categories = [
        "phishing",
        "password",
        "network",
        "malware",
        "social-engineering",
        "general"
    ]

    return render_template(
        "quiz/list.html",
        questions=questions,
        difficulties=difficulties,
        categories=categories,
        selected_difficulty=difficulty,
        selected_category=category
    )


# =====================================================
# Start Quiz
# =====================================================

@bp.route("/start")
@login_required
def start_quiz():

    difficulty = request.args.get(
        "difficulty",
        "easy"
    )

    category = request.args.get(
        "category",
        ""
    )

    num_questions = int(
        request.args.get(
            "num",
            10
        )
    )

    query = QuizQuestion.query.filter(
        QuizQuestion.is_active == True
    )

    if difficulty:
        query = query.filter(
            QuizQuestion.difficulty == difficulty
        )

    if category:
        query = query.filter(
            QuizQuestion.category == category
        )

    questions = query.order_by(
        func.rand()
    ).limit(num_questions).all()

    if not questions:

        flash(
            "No quiz questions available.",
            "warning"
        )

        return redirect(
            url_for("quiz.list_quizzes")
        )

    return render_template(
        "quiz/start.html",
        questions=questions,
        difficulty=difficulty,
        category=category
    )


# =====================================================
# Submit Quiz
# =====================================================

@bp.route("/submit", methods=["POST"])
@login_required
def submit_quiz():

    data = request.get_json()

    answers = data.get(
        "answers",
        {}
    )

    total_score = 0
    correct_count = 0

    results = []

    for question_id, selected_option in answers.items():

        question = QuizQuestion.query.get(
            int(question_id)
        )

        if not question:
            continue

        is_correct = (
            selected_option ==
            question.correct_option
        )

        points = 0

        if is_correct:

            points = (
                question.points
                if question.points
                else 10
            )

            correct_count += 1

        total_score += points

        score = QuizScore(
            user_id=current_user.id,
            question_id=question.id,
            selected_option=selected_option,
            is_correct=is_correct,
            points=points
        )

        db.session.add(score)

        results.append({
            "question": question.question,
            "selected": selected_option,
            "correct": question.correct_option,
            "is_correct": is_correct,
            "points": points,
            "explanation": question.explanation
        })

    db.session.commit()

    percentage = 0

    if len(answers) > 0:

        percentage = round(
            (correct_count / len(answers)) * 100,
            2
        )

    return jsonify({
        "success": True,
        "score": total_score,
        "correct": correct_count,
        "total": len(answers),
        "percentage": percentage,
        "results": results
    })


# =====================================================
# Results
# =====================================================

@bp.route("/results")
@login_required
def quiz_results():

    scores = QuizScore.query.filter_by(
        user_id=current_user.id
    ).order_by(
        QuizScore.id.desc()
    ).all()

    total_points = sum(
        s.points or 0
        for s in scores
    )

    total_correct = sum(
        1
        for s in scores
        if s.is_correct
    )

    total_questions = len(scores)

    return render_template(
        "quiz/results.html",
        scores=scores,
        total_points=total_points,
        total_correct=total_correct,
        total_questions=total_questions
    )


# =====================================================
# Leaderboard
# =====================================================

@bp.route("/leaderboard")
@login_required
def leaderboard():

    leaderboard_data = db.session.query(
        User.username,
        func.coalesce(
            func.sum(
                QuizScore.points
            ),
            0
        ).label(
            "total_points"
        )
    ).outerjoin(
        QuizScore,
        User.id == QuizScore.user_id
    ).group_by(
        User.id
    ).order_by(
        func.coalesce(
            func.sum(
                QuizScore.points
            ),
            0
        ).desc()
    ).limit(50).all()

    return render_template(
        "quiz/leaderboard.html",
        leaderboard=leaderboard_data
    )


# =====================================================
# AI Quiz Generator Page
# =====================================================

@bp.route("/generate")
@login_required
def ai_generator():

    return render_template(
        "quiz/ai_generate.html"
    )


# =====================================================
# AI Quiz Generator (Groq)
# =====================================================

@bp.route("/ai-generate", methods=["POST"])
@login_required
def ai_generate():

    try:

        data = request.get_json()

        topic = data.get(
            "topic",
            "Cyber Security"
        )

        quiz_type = data.get(
            "quiz_type",
            "MCQ"
        )

        quiz_level = data.get(
            "quiz_level",
            "Medium"
        )

        question_count = data.get(
            "question_count",
            10
        )

        if quiz_type == "MCQ":

            prompt = f"""
        Generate exactly {question_count} MCQ questions.

        Topic:
        {topic}

        Difficulty:
        {quiz_level}

        Rules:
        - Only MCQ
        - 4 options
        - Single correct answer
        - No MSQ
        - No NAT

        Format:

        Q1.
        Question

        A)
        B)
        C)
        D)

        Answer:
        """

        elif quiz_type == "MSQ":

            prompt = f"""
        Generate exactly {question_count} MSQ questions.

        Topic:
        {topic}

        Difficulty:
        {quiz_level}

        Rules:
        - Only MSQ
        - Multiple correct answers
        - No MCQ
        - No NAT

        Format:

        Q1.
        Question

        A)
        B)
        C)
        D)

        Correct Answers:
        A,C
        """

        elif quiz_type == "NAT":

            prompt = f"""
        Generate exactly {question_count} NAT questions.

        Topic:
        {topic}

        Difficulty:
        {quiz_level}

        STRICT RULES:

        - NAT ONLY
        - NO OPTIONS
        - NO MCQ
        - NO MSQ
        - Numerical Answer Required

        Format:

        Q1.
        Question

        Answer: 10

        Q2.
        Question

        Answer: 256
        """

        else:

            prompt = f"""
        Generate exactly {question_count} questions.

        Topic:
        {topic}

        Difficulty:
        {quiz_level}

        Distribution:

        40% MCQ
        40% MSQ
        20% NAT

        Give answer key at end.
        """
        answer = CyberShieldAI.ask(
            prompt
        )

        return jsonify({
            "success": True,
            "quiz": answer
        })

    except Exception as e:

        print("AI Generate Error:", e)

        return jsonify({
            "success": False,
            "quiz": str(e)
        })


# =====================================================
# Legacy AI Quiz Generator
# =====================================================

@bp.route("/generate-ai", methods=["POST"])
@login_required
def generate_ai():

    try:

        data = request.get_json()

        topic = data.get(
            "topic",
            "cybersecurity"
        )

        difficulty = data.get(
            "difficulty",
            "easy"
        )

        result = generate_quiz(
            topic,
            difficulty,
            5
        )

        return jsonify({
            "success": True,
            "result": result
        })

    except Exception as e:

        print("Generate AI Error:", e)

        return jsonify({
            "success": False,
            "result": str(e)
        })