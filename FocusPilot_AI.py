# FocusPilot AI
# Daily AI Study Assistant
# Generates, stores, and emails study plans automatically

import datetime
import json
import smtplib
from email.message import EmailMessage

from google import genai
from config import GEMINI_API_KEY, EMAIL_ADDRESS, EMAIL_PASSWORD, TO_EMAIL

client = genai.Client(api_key=GEMINI_API_KEY)

today = datetime.date.today()
day = today.weekday()
mode = "Intense Study Day" if day < 5 else "Light Learning Day"
prompt = f"""
You are an AI study assistant.

Date: {today}
Mode: {mode}

Tasks:
1. Create a short daily study plan for a beginner engineering student.
2. Include Python + one core engineering subject.
3. End with one motivational line.
"""

response = client.models.generate_content(
    model="models/gemini-2.5-flash",   
    contents=prompt
)

text = response.text

print("\n===== AI GENERATED PLAN =====\n")
print(text)

try:
    with open("memory.json", "r") as f:
        memory = json.load(f)
except:
    memory = []

memory.append({
    "date": str(today),
    "content": text
})

with open("memory.json", "w") as f:
    json.dump(memory, f, indent=2)

email = EmailMessage()
email["Subject"] = f"AI Daily Study Plan – {today}"
email["From"] = EMAIL_ADDRESS
email["To"] = TO_EMAIL
email.set_content(text)

try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(email)
        print("\n✅ Email sent successfully")
except Exception as e:
    print("\n❌ Email error:", e)

print("\n✅ AI Agent finished successfully")
