from services.ai_service import CyberShieldAI


class InterviewReportAI:

    @staticmethod
    def generate(history):

        prompt = f"""
Generate professional interview report.

History:

{history}

Return:

Overall Score

Strengths

Weaknesses

Placement Readiness %

Recommendations
"""

        return CyberShieldAI.ask(prompt)