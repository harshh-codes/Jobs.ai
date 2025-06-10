import fitz  # PyMuPDF
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Data model for comparison results
class MatchReport(BaseModel):
    Skill_Match: list[str]
    Missing_Skills: list[str]
    Experience_Relevance: str
    Overall_Match_Score: int  # Score from 1 to 10

# Extract text from PDF
def extract_text_from_pdf(pdf_path: str) -> str:
    doc = fitz.open(pdf_path)
    return "\n".join(page.get_text() for page in doc)

# Set up Gemini model
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)

# Set up output parser
parser = PydanticOutputParser(pydantic_object=MatchReport)

# Prompt template for comparison
prompt = ChatPromptTemplate.from_messages([
    ("system", """
    You are a resume matcher agent.
    Compare the following Resume and Job Description.

    1. Extract key skills from the resume.
    2. Extract required skills from the job description.
    3. Identify which resume skills match the job description.
    4. List missing skills from the resume that are required in the job.
    5. Assess whether the experience mentioned is relevant to the job.
    6. Return an overall match score from 1 to 10.

    Format your response in the following JSON format:
    {{
        "Skill_Match": ["skill1", "skill2", ...],
        "Missing_Skills": ["missing1", "missing2", ...],
        "Experience_Relevance": "...",
        "Overall_Match_Score": int
    }}

    Resume:
    {resume_text}

    Job Description:
    {job_description}

    Return ONLY the JSON.
    {format_instructions}
    """),
    ("user", "Resume: {resume_text}\n\nJob: {job_description}"),
    ("placeholder", "{agent_scratchpad}")
]).partial(format_instructions=parser.get_format_instructions())

# No tools required for this agent
tools = []

# Create the job matcher agent
agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Main function to run the matcher
def run_job_matcher(resume_pdf_path: str, job_description: str):
    resume_text = extract_text_from_pdf(resume_pdf_path)
    response = agent_executor.invoke({
        "resume_text": resume_text,
        "job_description": job_description
    })
    return response
