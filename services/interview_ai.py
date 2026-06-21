from services.ai_service import CyberShieldAI


class InterviewAI:

    @staticmethod
    def generate_question(role, level="medium"):

        prompt = f"""
You are a professional HR and Technical Interviewer.

Role:
{role}

Difficulty:
{level}

Ask ONLY ONE interview question.

No explanation.
No answer.

Return only question.
"""

        return CyberShieldAI.ask(prompt)

    @staticmethod
    def evaluate_answer(
        role,
        question,
        answer
    ):

        prompt = f"""
You are senior interviewer.

Role:
{role}

Question:
{question}

Candidate Answer:
{answer}

Evaluate answer.

Return:

Score: /10

Strengths:

Weaknesses:

Correct Answer:

Improvement Tips:
"""

        return CyberShieldAI.ask(prompt)