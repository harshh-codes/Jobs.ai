import smtplib
import os
import ssl
import re
from email.message import EmailMessage
from dotenv import load_dotenv

# Load email credentials from .env
load_dotenv()
EMAIL_ADDRESS = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASS")

# ✅ Extract email from resume using regex
def extract_email_from_resume(text: str) -> str:
    match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", text)
    return match.group(0) if match else "unknown@example.com"

# ✅ Extract name from resume (first line heuristic)
# def extract_name_from_resume(text: str) -> str:
#     for line in text.splitlines():
#         line = line.strip()
#         if line and all(word.istitle() for word in line.split() if word.isalpha()):
#             return line
#     return "Candidate"

# ✅ Send email only if score >= 5
def send_match_email(resume_text: str,candidate_name: str, match_score: int):
    if match_score < 5:
        print(f"❌ Match score too low ({match_score}/10), email not sent.")
        return

    to_email = extract_email_from_resume(resume_text)
    # candidate_name = extract_name_from_resume(resume_text)

    subject = "You're a great match for the job!"
    body = f"""
    Dear {candidate_name},

    Congratulations! Your resume has been reviewed and matches well with the job role.

    ✅ Match Score: {match_score}/10

    We would love to move forward and discuss this opportunity with you.

    Regards,  
    AI Agent Team
    """

    msg = EmailMessage()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
            print(f"✅ Email sent to {to_email}")
    except Exception as e:
        print(f"❌ Email failed: {e}")
