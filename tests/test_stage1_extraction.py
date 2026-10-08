from src.stage1_extraction.contact import extract_contact_info
from src.stage1_extraction.technical_skills import (
    extract_programming_languages,
    extract_frameworks,
    extract_databases,
    extract_tools,
)


def load_sample(name):
    with open(f"data/sample_resumes/{name}") as f:
        return f.read()


def test_extracts_email_from_wednesday_resume():
    text = load_sample("wednesday_addams.txt")
    contact = extract_contact_info(text)
    assert contact.get("email") == "wednesday.addams@nevermore.edu"


def test_extracts_phone_from_wednesday_resume():
    text = load_sample("wednesday_addams.txt")
    contact = extract_contact_info(text)
    assert contact.get("phone") == "+57 300 555 0199"


def test_missing_contact_fields_are_left_out():
    text = "Just a name with no contact info in it."
    contact = extract_contact_info(text)
    assert "email" not in contact
    assert "phone" not in contact


def test_extracts_full_stack_skills_from_wednesday_resume():
    text = load_sample("wednesday_addams.txt")
    assert extract_programming_languages(text) == ["JS"]
    assert extract_frameworks(text) == ["React.js", "NodeJS"]
    assert extract_databases(text) == ["Postgres"]
    assert extract_tools(text) == ["Git"]


def test_extracts_ml_engineer_skills_from_mary_jane_resume():
    text = load_sample("mary_jane_watson.txt")
    assert extract_programming_languages(text) == ["Python"]
    assert extract_frameworks(text) == ["Pandas", "NumPy", "Scikit-learn", "TensorFlow"]
    assert extract_databases(text) == ["SQL"]
    assert extract_tools(text) == ["Git"]


def test_dotted_framework_names_are_not_also_read_as_a_language():
    text = "Skills: React.js, Vue.js, Node.js"
    assert extract_programming_languages(text) == []
