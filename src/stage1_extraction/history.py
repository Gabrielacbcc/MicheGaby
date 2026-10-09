import re

EDUCATION_ENTRY = re.compile(
    r"^(?P<degree>.+?)\s-\s(?P<institution>.+?)\s\((?P<year>\d{4})\)\s*$"
)

EXPERIENCE_ENTRY = re.compile(
    r"^(?P<role>.+?)\s-\s(?P<company>.+?)\s\((?P<duration>\d+\syears?)\)\s*$"
)


def _section_lines(text, header):
    """Returns the lines that sit right under a section header such as
    'Education:' or 'Experience:', stopping at the first blank line or the
    end of the text, whichever comes first. The header line itself is not
    included.
    """
    lines = text.splitlines()
    try:
        start = lines.index(header) + 1
    except ValueError:
        return []

    section = []
    for line in lines[start:]:
        if line.strip() == "":
            break
        section.append(line.strip())
    return section


def extract_education(text):
    entries = []
    for line in _section_lines(text, "Education:"):
        match = EDUCATION_ENTRY.match(line)
        if match:
            entries.append(match.groupdict())
    return entries


def extract_experience(text):
    entries = []
    for line in _section_lines(text, "Experience:"):
        match = EXPERIENCE_ENTRY.match(line)
        if match:
            entries.append(match.groupdict())
    return entries
