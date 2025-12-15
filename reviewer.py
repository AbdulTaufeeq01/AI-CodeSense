import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"

def review_code(context):
    prompt = f"""
You are a senior software reviewer.
Identify bugs, security risks, and code smells.
Also provide suggested refactoring improvements.

Code:
{context}

Return concise bullet points organized in sections:
- Bugs and Issues
- Security Risks
- Code Smells
- Suggested Refactoring
"""
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json()["response"]
