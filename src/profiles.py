# These functions help get profile names, find technologies, and sort them

FULL_STACK = "FULL_STACK_DEVELOPER"
MACHINE_LEARNING = "MACHINE_LEARNING_ENGINEER"
DEVOPS = "DEVOPS_ENGINEER"
DATA_ENGINEER = "DATA_ENGINEER"

PROFILES = {
    FULL_STACK: [
        ("Frontend", "language", ["JAVASCRIPT", "TYPESCRIPT"]),
        ("Frontend", "ui framework", ["REACT", "ANGULAR", "VUE"]),
        ("Backend", "backend technology", ["NODE_JS", "DJANGO", "SPRING_BOOT"]),
        ("Backend", "api", ["REST_API"]),
        ("Database", "database", ["POSTGRESQL", "MYSQL", "MONGODB", "SQL", "NOSQL"]),
        ("Version control", "version control", ["GIT"]),
    ],
    MACHINE_LEARNING: [
        ("Language", "language", ["PYTHON"]),
        ("Data processing", "data library", ["PANDAS", "NUMPY"]),
        ("Machine learning", "classic ml library", ["SCIKIT_LEARN"]),
        ("Machine learning", "deep learning library", ["TENSORFLOW", "PYTORCH"]),
        ("Machine learning", "model development", ["ML_MODEL_DEVELOPMENT"]),
        ("Database", "database", ["SQL", "POSTGRESQL", "MYSQL"]),
        ("Version control", "version control", ["GIT"]),
    ],
    DEVOPS: [
        ("Operating system", "operating system", ["LINUX"]),
        ("Containers", "container runtime", ["DOCKER"]),
        ("Containers", "orchestration", ["KUBERNETES"]),
        ("Automation", "ci/cd", ["JENKINS", "GITHUB_ACTIONS"]),
        ("Automation", "infrastructure as code", ["TERRAFORM", "ANSIBLE"]),
        ("Cloud", "cloud provider", ["AWS", "AZURE", "GCP"]),
        ("Monitoring", "monitoring", ["PROMETHEUS", "GRAFANA"]),
        ("Version control", "version control", ["GIT"]),
    ],
    DATA_ENGINEER: [
        ("Language", "language", ["PYTHON"]),
        ("Database", "database", ["SQL", "POSTGRESQL", "MYSQL"]),
        ("Pipelines", "orchestration", ["AIRFLOW"]),
        ("Pipelines", "distributed processing", ["SPARK"]),
        ("Storage", "data warehouse", ["SNOWFLAKE", "BIGQUERY", "REDSHIFT"]),
        ("Version control", "version control", ["GIT"]),
    ],
}

def profile_names():
    return list(PROFILES)

# Returns every canonical token that matters for the profile
def profile_vocabulary(profile):
    return [t for _, _, tokens in PROFILES[profile] for t in tokens]

# Gives each token a position so the program can sort them
def token_rank(profile):
    rank = {}
    for i, (_, _, tokens) in enumerate(PROFILES[profile]):
        for j, token in enumerate(tokens):
            rank[token] = (i, j)
    return rank