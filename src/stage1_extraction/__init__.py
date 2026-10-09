from src.models import ResumeData
from src.stage1_extraction.contact import extract_contact_info
from src.stage1_extraction.technical_skills import (
    extract_programming_languages,
    extract_frameworks,
    extract_databases,
    extract_tools,
)
from src.stage1_extraction.history import extract_education, extract_experience


def extract_all(text):
    """Runs every Stage 1 extractor on the same resume text and groups the
    results into a single ResumeData object, which is what the rest of the
    pipeline expects as the output of this stage.
    """
    return ResumeData(
        contact=extract_contact_info(text),
        programming_languages=extract_programming_languages(text),
        frameworks=extract_frameworks(text),
        databases=extract_databases(text),
        tools=extract_tools(text),
        education=extract_education(text),
        experience=extract_experience(text),
    )
