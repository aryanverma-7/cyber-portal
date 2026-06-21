import requests

response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model":"llama3:8b",
        "prompt":"What is phishing?",
        "stream":False
    }
)

print(response.json())