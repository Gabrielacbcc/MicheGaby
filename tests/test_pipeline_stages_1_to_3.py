from src.pipeline import analyze_resume
from src.profiles import FULL_STACK, MACHINE_LEARNING, DEVOPS, DATA_ENGINEER


def load_sample(name):
    with open(f"data/sample_resumes/{name}") as f:
        return f.read()


def accepted_profiles(sample):
    result = analyze_resume(load_sample(sample))
    return [p for p, ok in result.classification.items() if ok]


def test_each_sample_is_accepted_only_by_its_own_profile():
    assert accepted_profiles("wednesday_addams.txt") == [FULL_STACK]
    assert accepted_profiles("mary_jane_watson.txt") == [MACHINE_LEARNING]
    assert accepted_profiles("marcus_reyes.txt") == [DEVOPS]
    assert accepted_profiles("elena_torres.txt") == [DATA_ENGINEER]


def test_normalized_sequence_of_the_guide_example():
    result = analyze_resume(load_sample("wednesday_addams.txt"))
    assert result.normalized[FULL_STACK] == [
        "JAVASCRIPT", "REACT", "NODE_JS", "REST_API", "POSTGRESQL", "GIT",
    ]


def test_resume_without_skills_is_rejected_everywhere():
    result = analyze_resume("Some Name\nNo skills listed here.")
    assert not any(result.classification.values())


def test_a_profile_can_be_checked_on_its_own():
    result = analyze_resume(load_sample("wednesday_addams.txt"), profiles=[FULL_STACK])
    assert list(result.classification) == [FULL_STACK]