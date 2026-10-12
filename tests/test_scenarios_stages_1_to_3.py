from src.pipeline import analyze_resume
from src.profiles import FULL_STACK, MACHINE_LEARNING, DATA_ENGINEER

def accepted(text):
    result = analyze_resume(text)
    return [p for p, ok in result.classification.items() if ok]


def test_s1_messy_spellings_are_normalized():
    text = "Ana Ruiz\n\nTechnical Skills:\njavascript, ReactJS, Node.js, PostgreSQL, restful apis, git."
    result = analyze_resume(text)
    assert result.normalized[FULL_STACK] == [
        "JAVASCRIPT", "REACT", "NODE_JS", "REST_API", "POSTGRESQL", "GIT",
    ]
    assert accepted(text) == [FULL_STACK]

def test_s2_alternative_technologies_are_accepted():
    text = "Leo Paz\n\nTechnical Skills:\nTypeScript, Vue.js, Django, MongoDB, REST API, Git."
    assert accepted(text) == [FULL_STACK]


def test_s3_missing_version_control_is_rejected():
    text = "Eva Lund\n\nTechnical Skills:\nJS, React, NodeJS, REST APIs, Postgres."
    assert accepted(text) == []


def test_s4_unrelated_extra_skills_do_not_change_the_result():
    text = ("Sam Roe\n\nTechnical Skills:\n"
            "JS, React.js, NodeJS, Postgres, REST APIs, Git, Docker, Python.")
    assert accepted(text) == [FULL_STACK]


def test_s5_a_single_skill_is_not_enough():
    assert accepted("Kim Oh\n\nTechnical Skills:\nPython.") == []


def test_s6_two_options_of_one_category_are_accepted():
    text = ("Zoe Ray\n\nTechnical Skills:\nPython, Pandas, NumPy, sklearn, PyTorch, "
            "TensorFlow, ML model development, Postgres, Git.")
    assert accepted(text) == [MACHINE_LEARNING]


def test_s7_order_in_the_resume_does_not_matter():
    text = "Ian Fox\n\nTechnical Skills:\nGit, SQL, Spark, Airflow, BigQuery, Python."
    assert accepted(text) == [DATA_ENGINEER]


def test_s8_text_without_skills_is_rejected_everywhere():
    result = analyze_resume("Just text.")
    assert not any(result.classification.values())
    assert result.resume.name == ""
