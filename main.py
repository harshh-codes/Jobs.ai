import json
import re
from agents.cv_parser import run_cv_parser
from agents.job_matcher import run_job_matcher, extract_text_from_pdf
from agents.email_agent import send_match_email

def main():
    resume_path = "Harsh Resume.pdf"
    job_path = "job_description.txt"

    # Read job description text
    with open(job_path, "r", encoding="utf-8") as f:
        job_description = f.read()

    # Extract resume info
    parsed_cv = run_cv_parser(resume_path)
    candidate_name = parsed_cv.get('Name', 'Candidate')  # Use fallback
    resume_text = extract_text_from_pdf(resume_path)

    # Run job matcher agent
    raw_report = run_job_matcher(resume_path, job_description)
    raw_output = raw_report.get("output", "")

    # ✅ Strip markdown formatting like ```json ... ```
    cleaned_output = re.sub(r"^```json\s*|\s*```$", "", raw_output.strip())

    # ✅ Safely handle empty or invalid JSON output
    if not cleaned_output:
        print("❌ ERROR: Job matcher output is empty or improperly formatted.")
        return

    try:
        match_report = json.loads(cleaned_output)
    except json.JSONDecodeError as e:
        print("❌ JSON Decode Error:", str(e))
        print("Raw cleaned output was:", repr(cleaned_output))
        return

    # Access values safely
    match_score = match_report.get('Overall_Match_Score', 0)

    # Print to console
    print(f"\nCandidate: {candidate_name}")
    print(f"Match Score: {match_score}/10")
    print("Skill Match:", match_report.get('Skill_Match', []))
    print("Missing Skills:", match_report.get('Missing_Skills', []))

    # Send email
    send_match_email(resume_text, candidate_name, match_score)

if __name__ == "__main__":
    main()
