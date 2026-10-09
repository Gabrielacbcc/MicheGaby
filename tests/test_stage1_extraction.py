from src.stage1_extraction.contact import extract_contact_info
from src.stage1_extraction.technical_skills import (
    extract_programming_languages,
    extract_frameworks,
    extract_databases,
    extract_tools,
)
from src.stage1_extraction.history import extract_education, extract_experience


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


def test_extracts_single_education_entry_from_wednesday_resume():
    text = load_sample("wednesday_addams.txt")
    education = extract_education(text)
    assert education == [
        {
            "degree": "BSc in Computer Science",
            "institution": "Nevermore Academy",
            "year": "2024",
        }
    ]


def test_extracts_two_experience_entries_from_wednesday_resume():
    text = load_sample("wednesday_addams.txt")
    experience = extract_experience(text)
    assert len(experience) == 2
    assert experience[0]["role"] == "Web Application Developer"
    assert experience[1]["role"] == "Freelance Developer"


def test_education_and_experience_are_empty_without_those_sections():
    text = "Just a name with no education or experience sections."
    assert extract_education(text) == []
    assert extract_experience(text) == []


def test_extract_all_on_full_stack_resume():
    from src.stage1_extraction import extract_all

    text = load_sample("wednesday_addams.txt")
    data = extract_all(text)
    assert data.contact["email"] == "wednesday.addams@nevermore.edu"
    assert data.programming_languages == ["JS"]
    assert data.frameworks == ["React.js", "NodeJS"]
    assert data.databases == ["Postgres"]
    assert data.tools == ["Git"]
    assert len(data.education) == 1
    assert len(data.experience) == 2


def test_extract_all_on_devops_resume():
    from src.stage1_extraction import extract_all

    text = load_sample("marcus_reyes.txt")
    data = extract_all(text)
    assert data.programming_languages == []
    assert data.tools == ["Linux", "Docker", "Kubernetes", "Jenkins", "Terraform", "AWS", "Prometheus", "Git"]
    assert data.education[0]["institution"] == "Universidad del Valle"


def test_extract_all_on_data_engineer_resume():
    from src.stage1_extraction import extract_all

    text = load_sample("elena_torres.txt")
    data = extract_all(text)
    assert data.programming_languages == ["Python"]
    assert data.frameworks == ["Airflow", "Spark"]
    assert data.databases == ["SQL", "Snowflake"]
    assert data.experience[0]["role"] == "Data Engineer"
