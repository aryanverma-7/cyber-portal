from services.ai_service import CyberShieldAI

print("Testing Groq AI...\n")

response = CyberShieldAI.ask(
    "What is phishing?"
)

print(response)