import re

EMAIL_PATTERN = r"[\w.+-]+@[\w-]+\.[\w.-]+"
PHONE_PATTERN = r"(?:\+?\d{1,3}[\s-]?)?\d{3}[\s-]?\d{3}[\s-]?\d{4}"


def extract_contact_info(text):
    """Finds an email address and a phone number somewhere in the text.

    Both patterns are searched independently, so one field can be found
    without the other, and neither is assumed to sit at a fixed position
    in the resume. A field that is not found is simply left out of the
    returned dictionary instead of being set to None.
    """
    contact = {}

    email_match = re.search(EMAIL_PATTERN, text)
    if email_match:
        contact["email"] = email_match.group()

    phone_match = re.search(PHONE_PATTERN, text)
    if phone_match:
        contact["phone"] = phone_match.group()

    return contact
