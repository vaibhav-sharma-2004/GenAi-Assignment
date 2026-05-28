from google import genai
import json
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

prompt = """
User activity:
- User A logged in and purchased a laptop worth $1200
- User B logged in but did not make any purchase
- User C purchased a phone worth $800

Tasks:
1. Summarize user activity
2. Extract structured insights

Return output ONLY in valid JSON format:

{
  "summary": "...",
  "total_users": 3,
  "purchasing_users": 2,
  "total_revenue": 2000,
  "insights": [
    "...",
    "..."
  ]
}
"""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)

print("\nRaw LLM Output:\n")
print(response.text)

try:
    cleaned_response = response.text.strip()

    cleaned_response = cleaned_response.replace("```json", "")
    cleaned_response = cleaned_response.replace("```", "")

    data = json.loads(cleaned_response)

    print("\nFormatted Output:\n")

    print("Summary:", data["summary"])
    print("Total Users:", data["total_users"])
    print("Purchasing Users:", data["purchasing_users"])
    print("Total Revenue:", data["total_revenue"])

    print("\nInsights:")
    for insight in data["insights"]:
        print("-", insight)

except Exception as e:
    print("\nJSON Parsing Error:", e)