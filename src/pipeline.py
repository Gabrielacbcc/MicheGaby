from src.models import AnalysisResult
from src.profiles import profile_names
from src.stage1_extraction import extract_all
from src.stage2_normalization import normalize_all, sort_normalized
from src.stage3_recognition import classify
from src.stage4_grammar import build_profile_text, render_html, render_markdown, validate_profile

def analyze_resume(text, profiles=None):
    """Runs Stages 1 to 3 on one resume and returns an AnalysisResult.
    The same code handles every profile; the only thing that changes is the profile name we pass to the normalization and recognition stages"""
    
    profiles = profiles or profile_names()

    # Stage 1: regular expressions
    resume = extract_all(text)
    raw_terms = (
        resume.programming_languages
        + resume.frameworks
        + resume.databases
        + resume.tools
        + resume.other_qualifications
    )

    # Stage 2: one transducer and one canonical order per profile
    normalized = {
        profile: sort_normalized(normalize_all(raw_terms, profile), profile)
        for profile in profiles
    }

    # Stage 3: one automaton per profile
    classification = classify(normalized)
    return AnalysisResult(resume=resume, normalized=normalized, classification=classification)


def run_pipeline(resume_text, profiles=None, output="html"):
    """Single entry point of ResumeLens: raw resume text in, visualization out.

    Runs Stages 1 to 3 through analyze_resume, writes the result in the candidate
    profile DSL, validates it with the textX grammar (raising ProfileValidationError
    when a rule is broken) and renders the validated model as HTML or Markdown."""
    if output not in ("html", "markdown"):
        raise ValueError("output must be 'html' or 'markdown'")
    result = analyze_resume(resume_text, profiles)
    text = build_profile_text(result.resume, result.normalized, result.classification)
    model = validate_profile(text)
    return render_html(model) if output == "html" else render_markdown(model)
