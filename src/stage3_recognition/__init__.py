from pyformlang.finite_automaton import Symbol
from src.stage3_recognition.automaton import build_automaton

def accepts(sequence, profile):

    """Checks if the ordered technologies match the profile. It returns True or False"""

    automaton = build_automaton(profile)
    return automaton.accepts([Symbol(token) for token in sequence])

def classify(sequence_by_profile):

    """Takes each profile and its sequence, then checks if it is accepted"""
    return{
        profile: accepts(sequence, profile)
        for profile, sequence in sequence_by_profile.items()
    }
