import smtplib
import ssl
import re
from email.message import EmailMessage

# Extract email from resume text using regex
def extract_email_from_resume(text: str) -> str:
    match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", text)
    return match.group(0) if match else "unknown@example.com"

# Send email if match score is 5 or more
def send_match_email(resume_text: str, candidate_name: str, match_score: int):
    if match_score < 5:
        print(f"❌ Match score too low ({match_score}/10), email not sent.")
        return

    to_email = extract_email_from_resume(resume_text)
    
    sender_email = "youremail@gmail.com"  # Replace with your sender email
    sender_password = "your_app_password"  # Use app password if Gmail

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
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
            print(f"✅ Email sent to {to_email}")
    except Exception as e:
        print(f"❌ Email failed: {e}")
