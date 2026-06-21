import requests
import re


def analyze_phishing(text):

    prompt = f"""
You are a cybersecurity analyst.

Analyze this message.

Return ONLY:

Risk Level: LOW / MEDIUM / HIGH

Reasons:
- reason 1
- reason 2

Recommendation:
- recommendation

Message:
{text}
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "phi3:mini",
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )

    return response.json()["response"]


class PhishingDetector:

    def analyze_email(
        self,
        email_content,
        email_sender,
        email_subject
    ):

        ai_result = analyze_phishing(
            f"""
Sender: {email_sender}

Subject: {email_subject}

Message:
{email_content}
"""
        )

        risk_score = 20

        suspicious_words = [
            "urgent",
            "verify",
            "password",
            "bank",
            "click here",
            "login",
            "account suspended",
            "limited time"
        ]

        content = (
            email_subject +
            " " +
            email_content
        ).lower()

        for word in suspicious_words:

            if word in content:
                risk_score += 10

        risk_score = min(
            risk_score,
            100
        )

        is_phishing = risk_score >= 50

        return {
            "is_phishing": is_phishing,
            "risk_score": risk_score,
            "reasons": [ai_result]
        }

    def analyze_url(self, url):

        ai_result = analyze_phishing(
            f"Analyze this URL: {url}"
        )

        risk_score = 10

        suspicious_patterns = [
            "@",
            "login",
            "verify",
            "secure-update",
            "banking"
        ]

        for pattern in suspicious_patterns:

            if pattern in url.lower():
                risk_score += 20

        risk_score = min(
            risk_score,
            100
        )

        is_phishing = risk_score >= 50

        return {
            "is_phishing": is_phishing,
            "risk_score": risk_score,
            "reasons": [ai_result]
        }