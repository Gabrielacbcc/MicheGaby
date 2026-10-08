from src.stage1_extraction.contact import extract_contact_info


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
