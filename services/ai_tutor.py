from services.ai_service import CyberShieldAI


class AITutor:

    @staticmethod
    def explain(topic):

        prompt = f"""
You are an expert Cyber Security Trainer.

Explain:

{topic}

IMPORTANT:

Return ONLY HTML.

Never use:

**
###
---
===
markdown

Use:

<h2>
<h3>
<p>
<ul>
<li>

Format:

Topic Overview
Simple Explanation
Real World Example
Attack Example
Prevention Tips
Interview Question
"""

        return CyberShieldAI.ask_html(
            prompt
        )

    @staticmethod
    def generate_quiz(topic):

        prompt = f"""
Create 5 MCQs about:

{topic}

IMPORTANT:

Return ONLY HTML.

Use:

<h3>
<ol>
<li>

Provide answer after each question.

Do not use markdown.
"""

        return CyberShieldAI.ask_html(
            prompt
        )