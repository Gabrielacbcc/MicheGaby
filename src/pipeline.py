from src.models import AnalysisResult
from src.profiles import profile_names
from src.stage1_extraction import extract_all
from src.stage2_normalization import normalize_all, sort_normalized
from src.stage3_recognition import classify

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