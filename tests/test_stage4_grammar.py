import pytest

from src.pipeline import analyze_resume, run_pipeline
from src.profiles import DATA_ENGINEER, DEVOPS, FULL_STACK, MACHINE_LEARNING
from src.stage4_grammar import (
    ProfileValidationError,
    build_profile_text,
    render_html,
    render_markdown,
    validate_profile,
)


def load_sample(name):
    with open(f"data/sample_resumes/{name}", encoding="utf-8") as f:
        return f.read()


def valid_text(sample="wednesday_addams.txt"):
    r = analyze_resume(load_sample(sample))
    return build_profile_text(r.resume, r.normalized, r.classification)


def test_generated_text_is_valid_for_every_sample():
    for sample in ("wednesday_addams.txt", "mary_jane_watson.txt", "marcus_reyes.txt", "elena_torres.txt"):
        model = validate_profile(valid_text(sample))
        assert len(model.results) == 4


def test_model_exposes_repeated_elements():
    model = validate_profile(valid_text())
    assert model.name == '"Wednesday Addams"'
    assert len(model.experience.entries) == 2
    assert [q.profile for q in model.qualifications][0] == FULL_STACK


def test_verdicts_follow_the_automata():
    model = validate_profile(valid_text("marcus_reyes.txt"))
    verdicts = {r.profile: r.status for r in model.results}
    assert verdicts[DEVOPS] == "ACCEPTED"
    assert verdicts[FULL_STACK] == verdicts[MACHINE_LEARNING] == verdicts[DATA_ENGINEER] == "REJECTED"


def test_unnamed_candidate_is_allowed():
    model = validate_profile(valid_text().replace('candidate "Wednesday Addams"', "candidate unnamed"))
    assert model.unnamed


@pytest.mark.parametrize("old,new", [
    ("email: wednesday.addams@nevermore.edu;", "email: not-an-email;"),          # lexical: Email
    ("year 2024;", "year 24;"),                                                   # lexical: Year
    ("for 3 years;", "for three years;"),                                         # lexical: Duration
    ("JAVASCRIPT, REACT", "javascript, REACT"),                                   # lexical: Token
    ("profile DATA_ENGINEER: REJECTED;", "profile DATA_ENGINEER: MAYBE;"),        # syntactic: Status
    ("contact {", "contactos {"),                                                 # syntactic: keyword
    ("  profile DEVOPS_ENGINEER: REJECTED;\n", ""),                               # missing verdict
])
def test_grammar_rejects_rule_violations(old, new):
    text = valid_text()
    assert old in text
    with pytest.raises(ProfileValidationError):
        validate_profile(text.replace(old, new))


def test_rejects_token_outside_profile_alphabet():
    text = valid_text().replace("{ GIT }", "{ GIT, JAVASCRIPT }", 1)
    with pytest.raises(ProfileValidationError, match="alphabet"):
        validate_profile(text)


def test_rejects_verdict_that_contradicts_automaton():
    text = valid_text().replace("profile FULL_STACK_DEVELOPER: ACCEPTED;", "profile FULL_STACK_DEVELOPER: REJECTED;")
    with pytest.raises(ProfileValidationError, match="automaton"):
        validate_profile(text)


def test_rejects_duplicated_profile_block():
    text = valid_text().replace("  profile FULL_STACK_DEVELOPER", "  qualifications FULL_STACK_DEVELOPER { GIT }\n  profile FULL_STACK_DEVELOPER")
    with pytest.raises(ProfileValidationError):
        validate_profile(text)


def test_quotes_in_names_are_escaped_not_injected():
    r = analyze_resume("Ann O'Neil\nTechnical Skills:\nGit.")
    r.resume.name = 'Ann "the dev" Lee'
    model = validate_profile(build_profile_text(r.resume, r.normalized, r.classification))
    assert 'the dev' in render_markdown(model)


def test_html_escapes_content():
    r = analyze_resume(load_sample("wednesday_addams.txt"))
    r.resume.name = "<script>x</script>"
    model = validate_profile(build_profile_text(r.resume, r.normalized, r.classification))
    html = render_html(model)
    assert "<script>x</script>" not in html and "&lt;script&gt;" in html


def test_run_pipeline_html_and_markdown():
    text = load_sample("mary_jane_watson.txt")
    html = run_pipeline(text, output="html")
    md = run_pipeline(text, output="markdown")
    assert html.startswith("<!DOCTYPE html>") and "Machine Learning Engineer" in html
    assert "| Machine Learning Engineer | ACCEPTED |" in md


def test_run_pipeline_resume_without_skills():
    md = run_pipeline("Just text.", output="markdown")
    assert "Unnamed candidate" in md and "ACCEPTED" not in md


def test_run_pipeline_rejects_unknown_output():
    with pytest.raises(ValueError):
        run_pipeline("x", output="pdf")
