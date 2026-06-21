from services.ai_service import CyberShieldAI


class InterviewScoreAI:

    @staticmethod
    def calculate(
        question,
        answer
    ):

        prompt = f"""
You are a professional technical interviewer.

Question:
{question}

Candidate Answer:
{answer}

Evaluate answer strictly.

Return format:

Communication Score: X/10

Technical Score: X/10

Confidence Score: X/10

Correctness Score: X/10

Overall Score: X/10

Strengths:
-

Weaknesses:
-

Improvement Tips:
-
"""

        return CyberShieldAI.ask(prompt)