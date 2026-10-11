from functools import lru_cache

from pyformlang.finite_automaton import DeterministicFiniteAutomaton, State, Symbol

from src.profiles import PROFILES, profile_vocabulary

def automaton_definition(profile):

    """Builds an automaton for each profile, checking that all required categories appear in the correct order. 
    Each state shows how many categories have been covered, and the profile is only accepted when all categories are included"""

    categories = PROFILES[profile]
    states = [f"q{i}" for i in range(len(categories) + 1)]
    delta = {}
    for i, (_, _, tokens) in enumerate(categories):
        for token in tokens:
            delta[(states[i], token)] = states[i + 1]       # first one of the category
            delta[(states[i + 1], token)] = states[i + 1]   # extra ones of the same category
    return {
        "Q": states,
        "Sigma": profile_vocabulary(profile),
        "delta": delta,
        "q0": states[0],
        "F": [states[-1]],
    }

@lru_cache(maxsize=None)
def build_automaton(profile):

    """Builds the pyformlang DFA of the profile from its 5-tuple"""
    
    definition = automaton_definition(profile)
    dfa = DeterministicFiniteAutomaton()
    dfa.add_start_state(State(definition["q0"]))
    for final in definition["F"]:
        dfa.add_final_state(State(final))
    for (source, token), target in definition["delta"].items():
        dfa.add_transition(State(source), Symbol(token), State(target))
    return dfa