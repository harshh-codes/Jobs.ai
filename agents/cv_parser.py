import fitz  # PyMuPDF
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from .tools import search_tool

# Load API key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Model output structure
class ResearchResponse(BaseModel):
    Name: str
    Experience: list[str]
    Education: list[str]
    Skills: list[str]

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path: str) -> str:
    doc = fitz.open(pdf_path)
    return "\n".join(page.get_text() for page in doc)

# Set up Gemini LLM
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7)

# Output parser
parser = PydanticOutputParser(pydantic_object=ResearchResponse)

# Prompt template
prompt = ChatPromptTemplate.from_messages([
("system", """
Extract key information from the following CV and return it in this JSON format:
{{
    "Name": "Candidate name",
 "Email": "Candidate email",
    "Experience": [
        "Job 1: ...",
        "Job 2: ..."
    ],
    "Education": [
        "Degree 1: ...",
        "Degree 2: ..."
    ],
    "Skills": [
        "Skill 1: ...",
        "Skill 2: ..."
    ]
}}

CV Text:
{cv_text}

Return ONLY the JSON object.
{format_instructions}
"""),
    ("user", "{cv_text}"),
    ("placeholder", "{agent_scratchpad}")
]).partial(format_instructions=parser.get_format_instructions())

# Tools (if any)
tools = [tool for tool in [search_tool] if tool]

# Agent builder
agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Agent caller
def run_cv_parser(pdf_path: str):
    cv_text = extract_text_from_pdf(pdf_path)
    response = agent_executor.invoke({"cv_text": cv_text})
    return response
