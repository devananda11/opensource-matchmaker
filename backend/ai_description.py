from dotenv import load_dotenv
import os
from pathlib import Path
from google import genai

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def explain_issue(title, body):

    prompt = f"""
Explain this GitHub issue in simple terms for a beginner developer.

IMPORTANT:
- Use ONLY the information provided below
- Do NOT invent or assume anything
- If something is unclear, say "Not specified"
- summarise the issue and description you got then explain

Title: {title}
Description: {body}

Answer in:
1. What is the problem?
2. Why does it matter?
3. How to start solving it?
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        return response.text

    except Exception as e:
        print("GEMINI ERROR:", e)
        return f"Error: {str(e)}"