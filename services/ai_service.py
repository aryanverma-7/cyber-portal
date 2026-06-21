from groq import Groq
from dotenv import load_dotenv
import markdown
import os
import time
from models import db
from models.ai_cache import AICache


load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(
    api_key=API_KEY
)


class CyberShieldAI:

    @staticmethod
    def ask(prompt):

        try:

            question = prompt.lower().strip()
    
            cached = AICache.query.filter_by(
                question=question
            ).first()

            if cached:

                print("CACHE HIT")

                return cached.answer

            start = time.time()

            response = client.chat.completions.create(

                model="llama-3.1-8b-instant",

                messages=[

                    {
                        "role": "system",

                        "content": """
You are CyberShield AI.

Rules:

1. Give clean professional answers.
2. Use markdown formatting.
3. Use headings.
4. Use bullet points.
5. Use tables when required.
6. Explain in beginner-friendly language.
7. Avoid unnecessary symbols.
8. Format output similar to ChatGPT.
"""
                    },

                    {
                        "role": "user",
                        "content": prompt
                    }

                ],

                temperature=0.2,

                max_tokens=1500
            )

            print(
                f"AI Response Time: {round(time.time()-start,2)} sec"
            )

            answer = response.choices[0].message.content

            new_cache = AICache(
                        question=question,
                        answer=answer
                )

            db.session.add(new_cache)
            db.session.commit()

            return answer

        except Exception as e:

            print("AI Error:", e)

            return f"AI Error: {e}"


    @staticmethod
    def ask_html(prompt):

        try:

            start = time.time()

            response = client.chat.completions.create(

                model="llama-3.1-8b-instant",

                messages=[

                    {
                        "role": "system",

                        "content": """
You are CyberShield AI.

Rules:

1. Give clean professional answers.
2. Use markdown formatting.
3. Use headings.
4. Use bullet points.
5. Use tables when required.
6. Explain in beginner-friendly language.
7. Avoid unnecessary symbols.
8. Format output similar to ChatGPT.
"""
                    },

                    {
                        "role": "user",
                        "content": prompt
                    }

                ],

                temperature=0.2,

                max_tokens=1500
            )

            print(
                f"AI Response Time: {round(time.time()-start,2)} sec"
            )

            raw_response = (
                response
                .choices[0]
                .message
                .content
            )

            html_response = markdown.markdown(

                raw_response,

                extensions=[
                    "tables",
                    "fenced_code"
                ]
            )

            return html_response

        except Exception as e:

            print("AI Error:", e)

            return f"<p>{e}</p>"