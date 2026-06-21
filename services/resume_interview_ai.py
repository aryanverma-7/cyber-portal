from services.ai_service import CyberShieldAI


class ResumeInterviewAI:

    @staticmethod
    def analyze_resume(resume_text):

        prompt = f"""
Analyze this resume.

Resume:
{resume_text}

Extract:

1. Skills
2. Technologies
3. Projects
4. Certifications
5. Strength Areas

Return clean format.
"""

        return CyberShieldAI.ask(prompt)

    @staticmethod
    def generate_resume_question(resume_text):

        prompt = f"""
You are a senior interviewer.

Resume:

{resume_text}

Generate ONE interview question
based on resume.

Only question.
"""

        return CyberShieldAI.ask(prompt)