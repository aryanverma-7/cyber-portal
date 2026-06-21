import requests


def generate_quiz(
    topic,
    difficulty="easy",
    count=5
):

    prompt = f"""
Generate {count} multiple choice cybersecurity questions.

Topic:
{topic}

Difficulty:
{difficulty}

Return:

QUESTION:
question

A:
option

B:
option

C:
option

D:
option

ANSWER:
A/B/C/D

EXPLANATION:
short explanation
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3:8b",
            "prompt": prompt,
            "stream": False
        },
        timeout=180
    )

    return response.json()["response"]