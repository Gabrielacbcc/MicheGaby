from functools import lru_cache

from pyformlang.fst import FST

from src.profiles import profile_vocabulary
from src.stage2_normalization.variants import VARIANTS


def transducer_definition(token):
    states = ["q0"]
    delta = []
    omega = {}  # transition: list with the output symbols
    interior = {"": "q0"}  # text already read: state that represents it

    for spelling in VARIANTS[token]:
        current = "q0"
        prefix = ""
        for char in spelling[:-1]:
            prefix += char
            if prefix not in interior:
                # First time we see this text: create its state and its edge
                new_state = f"q{len(states)}"
                states.append(new_state)
                interior[prefix] = new_state
                delta.append((current, char, new_state))
                omega[(current, char, new_state)] = [] 
            current = interior[prefix]
        last = (current, spelling[-1], "qf")
        delta.append(last)
        omega[last] = [token]

    states.append("qf")
    sigma = sorted({char for spelling in VARIANTS[token] for char in spelling})
    return {
        "Q": states,
        "Sigma": sigma,
        "Gamma": [token],
        "delta": delta,
        "omega": omega,
        "q0": "q0",
        "F": ["qf"],
    }


# Builds the pyformlang transducer of one profile. It is the union of the
# small transducers of every token the profile cares about: they all start in
# the same q0 and keep their own states (renamed with the token).
@lru_cache(maxsize=None)
def build_transducer(profile):
    fst = FST()
    fst.add_start_state("q0")

    for token in profile_vocabulary(profile):
        definition = transducer_definition(token)

        def name(state, token=token):
            return state if state == "q0" else f"{token}_{state}"

        fst.add_final_state(name("qf"))
        for source, char, target in definition["delta"]:
            output = definition["omega"][(source, char, target)]
            fst.add_transition(name(source), char, name(target), output)
    return fst