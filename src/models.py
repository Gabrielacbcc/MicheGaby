from dataclasses import dataclass, field


@dataclass
class ResumeData:
    """Holds everything Stage 1 pulls out of a resume, before normalization.

    Stage 4 reads this same structure later to fill in the personal and
    contact fields of the candidate profile, so it lives here at the top
    level instead of inside stage1_extraction.
    """

    name: str = ""
    contact: dict = field(default_factory=dict)
    programming_languages: list = field(default_factory=list)
    frameworks: list = field(default_factory=list)
    databases: list = field(default_factory=list)
    tools: list = field(default_factory=list)
    other_qualifications: list = field(default_factory=list)
    education: list = field(default_factory=list)
    experience: list = field(default_factory=list)

@dataclass
class AnalysisResult:
    """Stores the results from stages 1 through 3.
    Stage 4 uses this information to create the candidate's profile. 
    "normalized" stores the sorted technologies for each profile, and "classification" indicates whether each profile is True or False"""

    resume: ResumeData
    normalized: dict = field(default_factory=dict)
    classification: dict = field(default_factory=dict)