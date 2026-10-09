# ResumeLens

Resume screening application based on formal language theory.
Integrative Task 1 — Discrete Structures and Computing III (2026-2), CSI Department, Universidad Icesi.

## Team members

- Mateo Cuenca
- Gabriela Cardona
- Jazmin Michelle Galvez

## Course

- Course Code: 09834
- Group: 3 (Andrés)

## Description

ResumeLens processes text resumes and determines whether the qualifications it identifies
satisfy formally defined patterns for a professional profile. It does not rank candidates
or make hiring decisions: it only evaluates whether the qualifications explicitly stated in
the resume satisfy an accepted qualification pattern.

The system applies the same general pipeline to all four supported profiles, going through
four distinct formal language models:

1. **Information extraction** — regular expressions (`re`)
2. **Qualification normalization** — finite state transducers (`pyformlang`)
3. **Qualification pattern recognition** — finite automata (`pyformlang`)
4. **Candidate profile language** — context-free grammar in EBNF (`textX`)

## Supported profiles

1. **Full Stack Developer** (fixed) — JavaScript/TypeScript, React/Angular/Vue, Node.js/Django/Spring Boot, SQL/NoSQL, REST APIs, Git
2. **Machine Learning Engineer** (fixed) — Python, Pandas/NumPy, Scikit-learn, TensorFlow/PyTorch, ML model development, SQL, Git
3. **DevOps Engineer** (additional — software engineering) — Linux, Docker, Kubernetes, CI/CD (Jenkins/GitHub Actions), Terraform/Ansible, cloud (AWS/Azure/GCP), monitoring (Prometheus/Grafana), Git
4. **Data Engineer** (additional — AI/data) — Python, SQL, pipeline orchestration (Airflow), distributed processing (Spark), data warehousing (Snowflake/BigQuery/Redshift), data formats (Parquet/JSON), Git

## Repository structure

```
ResumeLens/
├── README.md
├── requirements.txt
├── docs/ # Design documents (poster, literature review, formalization, test cases)
├── data/
│ └── sample_resumes/ # Sample resumes used to test the pipeline
├── src/
│ ├── stage1_extraction/ # Regular expressions
│ ├── stage2_normalization/ # Finite state transducers
│ ├── stage3_recognition/ # Finite automata
│ └── stage4_grammar/ # EBNF / textX grammar + visualization
└── tests/ # Scenario-based tests
```


## How to run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest tests/
```

## Tools

- IDE: VSCode
- Python: 3.10

## Submission

Deadline: October 11, 2026.
