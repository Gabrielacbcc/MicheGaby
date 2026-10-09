import re

PROGRAMMING_LANGUAGES = ["TypeScript", "JavaScript", "JS", "Python"]

# Specific, longer spellings first (React.js before React): alternation
# stops at the first option that matches, so a generic entry placed
# earlier would match inside the compound name and leave the rest unread.
FRAMEWORKS = [
    "React.js", "ReactJS", "React",
    "Angular",
    "Vue.js", "VueJS", "Vue",
    "Node.js", "NodeJS",
    "Spring Boot", "Django",
    "Pandas", "NumPy",
    "Scikit-learn", "scikit learn", "sklearn",
    "Tensor Flow", "TensorFlow",
    "Py Torch", "PyTorch",
    "Airflow", "Spark",
]

DATABASES = [
    "PostgreSQL", "Postgres",
    "MongoDB", "MySQL",
    "NoSQL", "SQL",
    "Snowflake", "BigQuery", "Redshift",
]

TOOLS = [
    "GitHub Actions", "Git",
    "Docker", "Kubernetes", "Jenkins",
    "Terraform", "Ansible",
    "Prometheus", "Grafana",
    "AWS", "Azure", "GCP",
    "Linux",
]

# Qualifications named in the reference profiles that are phrases, not a
# single tool or language name, so they don't belong in the lists above.
OTHER_QUALIFICATIONS = [
    "RESTful APIs", "REST APIs", "REST API", "RESTful API",
    "Machine-learning model development", "Machine Learning model development",
    "ML model development", "model development",
]


def _find_keywords(text, keywords):
    """Looks for any of the given raw spellings inside text and returns the
    ones that were actually found, in the order they first appear, without
    repeats. The keyword list should go from the most specific spelling to
    the most generic one (React.js before React), so a compound name is not
    cut short by a shorter alternative that also happens to match.

    A match is skipped when it is immediately preceded by a dot with no
    space before it, since that almost always means the match is really
    the tail end of a dotted name from another category, such as the "js"
    in "React.js", and not a standalone mention of that keyword.
    """
    pattern = r"\b(" + "|".join(re.escape(k) for k in keywords) + r")\b"
    found = []
    for match in re.finditer(pattern, text, re.IGNORECASE):
        start = match.start()
        # A dot right before the match means this is the tail of a dotted
        # name (the "js" in "React.js"), not a real standalone keyword.
        if start > 0 and text[start - 1] == ".":
            continue
        term = match.group()
        if term not in found:
            found.append(term)
    return found


def extract_programming_languages(text):
    return _find_keywords(text, PROGRAMMING_LANGUAGES)


def extract_frameworks(text):
    return _find_keywords(text, FRAMEWORKS)


def extract_databases(text):
    return _find_keywords(text, DATABASES)


def extract_tools(text):
    return _find_keywords(text, TOOLS)


def extract_other_qualifications(text):
    return _find_keywords(text, OTHER_QUALIFICATIONS)
