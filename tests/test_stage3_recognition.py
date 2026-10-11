from src.profiles import (PROFILES, FULL_STACK, MACHINE_LEARNING, DEVOPS, DATA_ENGINEER, profile_names)
from src.stage3_recognition import accepts, classify
from src.stage3_recognition.automaton import automaton_definition, build_automaton

FULL_STACK_OK = ["JAVASCRIPT", "REACT", "NODE_JS", "REST_API", "POSTGRESQL", "GIT"]
ML_OK = ["PYTHON", "PANDAS", "SCIKIT_LEARN", "TENSORFLOW", "ML_MODEL_DEVELOPMENT", "SQL", "GIT"]
DEVOPS_OK = ["LINUX", "DOCKER", "KUBERNETES", "JENKINS", "TERRAFORM", "AWS", "PROMETHEUS", "GIT"]
DATA_OK = ["PYTHON", "SQL", "AIRFLOW", "SPARK", "SNOWFLAKE", "GIT"]


def test_each_profile_accepts_its_complete_pattern():
    assert accepts(FULL_STACK_OK, FULL_STACK)
    assert accepts(ML_OK, MACHINE_LEARNING)
    assert accepts(DEVOPS_OK, DEVOPS)
    assert accepts(DATA_OK, DATA_ENGINEER)

def test_missing_category_is_rejected():
    assert not accepts([t for t in FULL_STACK_OK if t != "GIT"], FULL_STACK)
    assert not accepts([t for t in ML_OK if t != "PYTHON"], MACHINE_LEARNING)

def test_wrong_order_is_rejected():
    assert not accepts(["GIT", "JAVASCRIPT", "REACT", "NODE_JS", "REST_API", "POSTGRESQL"], FULL_STACK)

def test_empty_sequence_is_rejected():
    for profile in profile_names():
        assert not accepts([], profile)

def test_two_options_of_the_same_category_are_accepted():
    both = ["PYTHON", "PANDAS", "NUMPY", "SCIKIT_LEARN", "TENSORFLOW", "PYTORCH",
            "ML_MODEL_DEVELOPMENT", "SQL", "GIT"]
    assert accepts(both, MACHINE_LEARNING)

def test_alternatives_inside_a_category_work():
    assert accepts(["TYPESCRIPT", "VUE", "DJANGO", "REST_API", "MONGODB", "GIT"], FULL_STACK)

def test_automata_are_deterministic_and_use_the_whole_profile_alphabet():
    for profile in profile_names():
        assert build_automaton(profile).is_deterministic()
        definition = automaton_definition(profile)
        assert len(definition["Q"]) == len(PROFILES[profile]) + 1
        assert definition["F"] == [definition["Q"][-1]]

# Needed so the automaton never has two transitions for the same token
def test_categories_of_a_profile_do_not_share_tokens():
    for profile, categories in PROFILES.items():
        tokens = [t for _, _, ts in categories for t in ts]
        assert len(tokens) == len(set(tokens)), profile

def test_classify_returns_one_answer_per_profile():
    result = classify({FULL_STACK: FULL_STACK_OK, MACHINE_LEARNING: FULL_STACK_OK[:2]})
    assert result == {FULL_STACK: True, MACHINE_LEARNING: False}