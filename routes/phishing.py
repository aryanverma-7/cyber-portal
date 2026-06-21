from flask import (
    Blueprint,
    render_template,
    request,
    jsonify
)

from flask_login import (
    login_required,
    current_user
)

from models import db
from models.phishing import PhishingCase

from services.phishing_detector import (
    PhishingDetector,
    analyze_phishing
)

import json

bp = Blueprint(
    "phishing",
    __name__,
    url_prefix="/phishing"
)

# ==================================================
# Main Page
# ==================================================

@bp.route("/")
@login_required
def index():
    return render_template(
        "phishing/index.html"
    )


# ==================================================
# AI Detector Page
# ==================================================

@bp.route("/ai-detector")
@login_required
def ai_detector():

    return render_template(
        "phishing/ai_detector.html"
    )


# ==================================================
# AI Detector API
# ==================================================

@bp.route("/check-url", methods=["POST"])
@login_required
def check_url():

    data = request.get_json()

    url = data.get("url", "").lower()

    risk_score = 0
    reasons = []

    suspicious_words = [
        "login",
        "verify",
        "secure",
        "banking",
        "update",
        "paypal",
        "account"
    ]

    for word in suspicious_words:
        if word in url:
            risk_score += 20
            reasons.append(
                f"Contains suspicious keyword: {word}"
            )

    if "@" in url:
        risk_score += 30
        reasons.append(
            "Contains @ symbol"
        )

    if len(url) > 80:
        risk_score += 10
        reasons.append(
            "Very long URL"
        )

    return jsonify({
        "success": True,
        "risk_score": risk_score,
        "reasons": reasons
    })


# ==================================================
# Phishing Simulation Page
# ==================================================

@bp.route("/simulate")
@login_required
def simulate():

    return render_template(
        "phishing/simulator.html"
    )


# ==================================================
# Email Analysis
# ==================================================

@bp.route("/check-email", methods=["POST"])
@login_required
def check_email():

    data = request.get_json()

    sender = data.get("sender", "")
    subject = data.get("subject", "")
    content = data.get("content", "")

    score = 0
    reasons = []

    suspicious_phrases = [
        "urgent",
        "verify account",
        "click here",
        "limited time",
        "password expired",
        "bank account"
    ]

    text = (
        sender +
        subject +
        content
    ).lower()

    for phrase in suspicious_phrases:

        if phrase in text:

            score += 20

            reasons.append(
                f"Suspicious phrase: {phrase}"
            )

        is_phishing = score >= 40

        risk_level = (
            "High" if score >= 70
            else "Medium" if score >= 40
            else "Low"
        )

        return jsonify({
            "success": True,
            "is_phishing": is_phishing,
            "risk_score": score,
            "risk_level": risk_level,
            "reasons": reasons,
            "recommendation":
                "Avoid interacting with this email."
                if is_phishing
                else
                "No major phishing indicators detected."
        })


# ==================================================
# URL Analysis
# ==================================================


# ==================================================
# User History
# ==================================================

@bp.route("/history")
@login_required
def history():

    cases = PhishingCase.query.filter(
        PhishingCase.user_id ==
        current_user.id
    ).order_by(
        PhishingCase.created_at.desc()
    ).limit(50).all()

    return render_template(
        "phishing/history.html",
        cases=cases
    )


# ==================================================
# Threat Dashboard
# ==================================================

@bp.route("/dashboard")
@login_required
def threat_dashboard():

    latest_threats = (
        PhishingCase.query
        .filter(
            PhishingCase.is_phishing == True
        )
        .order_by(
            PhishingCase.created_at.desc()
        )
        .limit(10)
        .all()
    )

    trending = (
        db.session.query(
            PhishingCase.email_subject,
            db.func.count(
                PhishingCase.id
            )
        )
        .filter(
            PhishingCase.is_phishing == True
        )
        .group_by(
            PhishingCase.email_subject
        )
        .order_by(
            db.func.count(
                PhishingCase.id
            ).desc()
        )
        .limit(10)
        .all()
    )

    total_checks = (
        PhishingCase.query
        .filter(
            PhishingCase.user_id ==
            current_user.id
        )
        .count()
    )

    phishing_detected = (
        PhishingCase.query
        .filter(
            PhishingCase.user_id ==
            current_user.id,
            PhishingCase.is_phishing == True
        )
        .count()
    )

    safe_emails = (
        total_checks -
        phishing_detected
    )

    risk_distribution = (
        db.session.query(
            PhishingCase.risk_score,
            db.func.count(
                PhishingCase.id
            )
        )
        .filter(
            PhishingCase.user_id ==
            current_user.id
        )
        .group_by(
            PhishingCase.risk_score
        )
        .all()
    )

    return render_template(
        "phishing/dashboard.html",
        latest_threats=latest_threats,
        trending=trending,
        total_checks=total_checks,
        phishing_detected=phishing_detected,
        safe_emails=safe_emails,
        risk_distribution=risk_distribution
    )