from dataclasses import dataclass, field


@dataclass
class ResumeData:
    """Holds everything Stage 1 pulls out of a resume, before normalization.

    Stage 4 reads this same structure later to fill in the personal and
    contact fields of the candidate profile, so it lives here at the top
    level instead of inside stage1_extraction.
    """

    contact: dict = field(default_factory=dict)
    programming_languages: list = field(default_factory=list)
    frameworks: list = field(default_factory=list)
    databases: list = field(default_factory=list)
    tools: list = field(default_factory=list)
    other_qualifications: list = field(default_factory=list)
    education: list = field(default_factory=list)
    experience: list = field(default_factory=list)
