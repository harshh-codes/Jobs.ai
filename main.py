from agents.job_matcher import run_job_matcher  # Adjust path as per your project structure

def main():
    # Path to the resume PDF
    resume_pdf_path = "Harsh Resume.pdf"  # <-- Replace with your actual path

    # Path to the job description .txt file
    job_description_file = "job_description.txt"  # <-- Replace with your actual file

    # Read job description from the text file
    with open(job_description_file, 'r', encoding='utf-8') as file:
        job_description = file.read()

    # Run the matcher agent
    match_report = run_job_matcher(resume_pdf_path, job_description)

    # Print the match report
    print("\nMatch Report:\n", match_report)

if __name__ == "__main__":
    main()
