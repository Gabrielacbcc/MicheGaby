from src.profiles import PROFILES, FULL_STACK, MACHINE_LEARNING, DEVOPS, DATA_ENGINEER
from src.stage2_normalization import (
    normalize_term,
    normalize_all,
    canonical_order,
    sort_normalized,
)
from src.stage2_normalization.transducer import build_transducer, transducer_definition
from src.stage2_normalization.variants import VARIANTS

# Any profile that uses this token is fine to test its spellings
def profile_with(token):
    for name, categories in PROFILES.items():
        if any(token in tokens for _, _, tokens in categories):
            return name

def test_every_spelling_maps_to_its_canonical_token():
    for token, spellings in VARIANTS.items():
        transducer = build_transducer(profile_with(token))
        for spelling in spellings:
            assert normalize_term(spelling, transducer) == (token, True), spelling

def test_guide_examples_for_full_stack():
    transducer = build_transducer(FULL_STACK)
    assert normalize_term("JS", transducer) == ("JAVASCRIPT", True)
    assert normalize_term("Javascript", transducer) == ("JAVASCRIPT", True)
    assert normalize_term("React.js", transducer) == ("REACT", True)
    assert normalize_term("ReactJS", transducer) == ("REACT", True)
    assert normalize_term("NodeJS", transducer) == ("NODE_JS", True)
    assert normalize_term("Node.js", transducer) == ("NODE_JS", True)
    assert normalize_term("Postgres", transducer) == ("POSTGRESQL", True)

def test_guide_examples_for_machine_learning():
    transducer = build_transducer(MACHINE_LEARNING)
    for raw in ["sklearn", "scikit learn", "Scikit-learn"]:
        assert normalize_term(raw, transducer) == ("SCIKIT_LEARN", True)
    for raw in ["Tensor Flow", "TensorFlow"]:
        assert normalize_term(raw, transducer) == ("TENSORFLOW", True)
    for raw in ["Py Torch", "PyTorch"]:
        assert normalize_term(raw, transducer) == ("PYTORCH", True)

def test_short_spelling_that_starts_a_longer_one():
    transducer = build_transducer(FULL_STACK)
    assert normalize_term("React", transducer) == ("REACT", True)
    assert normalize_term("react.js", transducer) == ("REACT", True)

def test_unknown_term_is_returned_unchanged_and_flagged():
    transducer = build_transducer(FULL_STACK)
    assert normalize_term("Docker", transducer) == ("Docker", False)
    assert normalize_term("reac", transducer) == ("reac", False)

def test_transducer_definition_is_a_complete_tuple():
    definition = transducer_definition("JAVASCRIPT")
    assert definition["q0"] in definition["Q"]
    assert set(definition["F"]) <= set(definition["Q"])
    assert definition["Gamma"] == ["JAVASCRIPT"]
    for source, char, target in definition["delta"]:
        assert source in definition["Q"] and target in definition["Q"]
        assert char in definition["Sigma"]
        assert (source, char, target) in definition["omega"]

def test_normalize_all_keeps_duplicates_and_unknown_terms():
    result = normalize_all(["JS", "Javascript", "Docker"], FULL_STACK)
    assert result == ["JAVASCRIPT", "JAVASCRIPT", "Docker"]

def test_canonical_order_of_full_stack():
    assert canonical_order(FULL_STACK) == ["Frontend", "Backend", "Database", "Version control"]

def test_sorting_example_from_the_guide():
    raw = ["Git", "NodeJS", "JS", "Postgres", "React.js"]
    normalized = normalize_all(raw, FULL_STACK)
    assert sort_normalized(normalized, FULL_STACK) == [
        "JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT",
    ]

def test_sorting_removes_repeated_and_unrelated_terms():
    terms = ["GIT", "DOCKER", "JAVASCRIPT", "GIT", "Unknown"]
    assert sort_normalized(terms, FULL_STACK) == ["JAVASCRIPT", "GIT"]

def test_order_does_not_depend_on_how_the_resume_was_written():
    a = normalize_all(["Python", "Git", "SQL", "Spark", "Airflow"], DATA_ENGINEER)
    b = normalize_all(["Airflow", "Spark", "Git", "Python", "SQL"], DATA_ENGINEER)
    assert sort_normalized(a, DATA_ENGINEER) == sort_normalized(b, DATA_ENGINEER)

def test_devops_variants():
    result = normalize_all(["k8s", "Amazon Web Services", "GitHub Actions"], DEVOPS)
    assert result == ["KUBERNETES", "AWS", "GITHUB_ACTIONS"]
