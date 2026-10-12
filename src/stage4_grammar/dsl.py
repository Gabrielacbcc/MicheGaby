import re
from functools import lru_cache
from pathlib import Path

from textx import metamodel_from_file
from textx.exceptions import TextXError

from src.profiles import PROFILES, profile_names, profile_vocabulary
from src.stage3_recognition import accepts

GRAMMAR_PATH = Path(__file__).with_name("candidate.tx")


class ProfileValidationError(ValueError):
    """Raised when a candidate profile text breaks a lexical, syntactic or semantic rule."""


def _quote(value):
    """Writes a Python string as a NameString terminal: double quotes, with
    backslash and quote escaped, and line breaks flattened to a space."""
    clean = " ".join(str(value).split())
    return '"' + clean.replace("\\", "\\\\").replace('"', '\\"') + '"'


def _unquote(literal):
    return re.sub(r"\\(.)", r"\1", literal[1:-1])


def build_profile_text(resume_data, normalized_by_profile, classification):
    """Writes the Stage 1 to 3 results as text in the candidate profile DSL.

    The text is only a candidate: it is not trusted until validate_profile
    parses it, so values that break the grammar are rejected there and not here."""
    lines = []
    if resume_data.name:
        lines.append(f"candidate {_quote(resume_data.name)} {{")
    else:
        lines.append("candidate unnamed {")

    lines.append("  contact {")
    for key in ("email", "phone"):
        if key in resume_data.contact:
            lines.append(f"    {key}: {resume_data.contact[key]};")
    lines.append("  }")

    lines.append("  education {")
    for e in resume_data.education:
        lines.append(
            f"    degree {_quote(e['degree'])} at {_quote(e['institution'])} year {e['year']};"
        )
    lines.append("  }")

    lines.append("  experience {")
    for e in resume_data.experience:
        lines.append(
            f"    role {_quote(e['role'])} at {_quote(e['company'])} for {e['duration']};"
        )
    lines.append("  }")

    for profile in normalized_by_profile:
        tokens = ", ".join(normalized_by_profile[profile])
        lines.append(f"  qualifications {profile} {{ {tokens} }}")
    for profile in classification:
        status = "ACCEPTED" if classification[profile] else "REJECTED"
        lines.append(f"  profile {profile}: {status};")
    lines.append("}")
    return "\n".join(lines)


@lru_cache(maxsize=1)
def _metamodel():
    return metamodel_from_file(str(GRAMMAR_PATH))


def _semantic_checks(model):
    """Rules a context-free grammar cannot express: every profile exactly once,
    tokens inside the vocabulary of their profile, and a verdict that agrees
    with the Stage 3 automaton."""
    seen = {}
    for q in model.qualifications:
        if q.profile in seen:
            raise ProfileValidationError(f"qualifications for {q.profile} appear twice")
        seen[q.profile] = list(q.tokens)
        vocabulary = set(profile_vocabulary(q.profile))
        for token in q.tokens:
            if token not in vocabulary:
                raise ProfileValidationError(
                    f"token {token} is not part of the alphabet of {q.profile}"
                )

    verdicts = {}
    for r in model.results:
        if r.profile in verdicts:
            raise ProfileValidationError(f"profile {r.profile} has two verdicts")
        verdicts[r.profile] = r.status == "ACCEPTED"

    expected = set(profile_names())
    if set(seen) != expected or set(verdicts) != expected:
        raise ProfileValidationError("every supported profile needs one qualifications block and one verdict")

    for profile, tokens in seen.items():
        if accepts(tokens, profile) != verdicts[profile]:
            raise ProfileValidationError(
                f"verdict of {profile} does not match its automaton on {tokens}"
            )


def validate_profile(profile_text):
    """Parses the text with the textX grammar and returns the model, or raises
    ProfileValidationError saying which rule was violated."""
    try:
        model = _metamodel().model_from_str(profile_text)
    except TextXError as error:
        raise ProfileValidationError(str(error)) from error
    _semantic_checks(model)
    return model


def model_to_dict(model):
    """Plain dictionary view of a validated model, used by the renderers."""
    return {
        "name": "" if model.unnamed else _unquote(model.name),
        "email": model.contact.email or "",
        "phone": model.contact.phone or "",
        "education": [
            {"degree": _unquote(e.degree), "institution": _unquote(e.institution), "year": e.year}
            for e in model.education.entries
        ],
        "experience": [
            {"role": _unquote(e.role), "company": _unquote(e.company), "duration": e.duration}
            for e in model.experience.entries
        ],
        "qualifications": {q.profile: list(q.tokens) for q in model.qualifications},
        "results": {r.profile: r.status == "ACCEPTED" for r in model.results},
    }
