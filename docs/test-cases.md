# Test Cases Design

This document covers the test design for Stages 1 to 3 of the pipeline: extraction, normalization and recognition. Unit tests check one function at a time; scenario tests push a whole resume through the pipeline and check the final answer.

## Test levels

| Level | Where | What it checks |
|-------|-------|----------------|
| Unit, Stage 1 | tests/test_stage1_extraction.py | Each regular expression and extractor on its own, including the missing field cases and the `React.js` versus `JS` regression. |
| Unit, Stage 2 | tests/test_stage2_normalization.py | Every spelling of every canonical token, the examples of the guide, unknown terms, sorting and the complete tuple of a transducer. |
| Unit, Stage 3 | tests/test_stage3_recognition.py | Accepted and rejected sequences, wrong order, empty input, alternatives inside a category, determinism of every automaton. |
| Integration | tests/test_pipeline_stages_1_to_3.py | The four sample resumes, each accepted only by its own profile. |
| Scenario | tests/test_scenarios_stages_1_to_3.py | The scenarios of the table below. |

## Sample data

The files in data/sample_resumes/ are the base of the integration tests: wednesday_addams.txt (Full Stack Developer) and mary_jane_watson.txt (Machine Learning Engineer) come from the guide, marcus_reyes.txt covers DevOps Engineer and elena_torres.txt covers Data Engineer.

## Scenarios (Stages 1 to 3)

| Id | Scenario | Input skills | Expected result |
|----|----------|--------------|-----------------|
| S1 | Messy spellings and letter case | javascript, ReactJS, Node.js, PostgreSQL, restful apis, git | Normalized to JAVASCRIPT, REACT, NODE_JS, REST_API, POSTGRESQL, GIT; Full Stack Developer ACCEPTED |
| S2 | Alternative technologies | TypeScript, Vue.js, Django, MongoDB, REST API, Git | Full Stack Developer ACCEPTED |
| S3 | Missing category | JS, React, NodeJS, REST APIs, Postgres (no Git) | Rejected by all four profiles |
| S4 | Unrelated extra skills | the Full Stack skills plus Docker and Python | Full Stack Developer ACCEPTED, the extra skills do not change the result |
| S5 | Too little information | Python only | Rejected by all four profiles |
| S6 | Two options of the same category | Python, Pandas, NumPy, sklearn, PyTorch, TensorFlow, ML model development, Postgres, Git | Machine Learning Engineer ACCEPTED |
| S7 | Skills written in a different order | Git, SQL, Spark, Airflow, BigQuery, Python | Data Engineer ACCEPTED, the same as in canonical order |
| S8 | Text without skills or name | "Just text." | Rejected by all four profiles, name is empty |

## Edge cases covered by unit tests

- A resume without email, phone, Education or Experience produces empty fields, not errors.
- `React.js`, `Vue.js` and `Node.js` are not also read as the language `JS`.
- A short spelling that begins a longer one (`react` and `react.js`) normalizes to the same token.
- A term the profile does not know (`Docker` for Full Stack Developer) is returned unchanged and flagged as not recognized.
- An empty sequence is rejected by every automaton.
- A sequence in the wrong order (`GIT` first) is rejected.
- No two categories of the same profile share a token, so every automaton stays deterministic.
