from src.profiles import PROFILES, token_rank
from src.stage2_normalization.transducer import build_transducer

# Gets the original value from symbols returned by pyformlang
def _plain(symbol):
    return getattr(symbol, "value", symbol)

def _translate(transducer, characters):
    limit = max(20, 2 * len(characters))
    try:
        return list(transducer.translate(characters, max_length=limit))
    except TypeError:  # Older versions do not support max_length
        return list(transducer.translate(characters))

def normalize_term(term, transducer):
    """Runs one raw term through the transducer.
    
    Returns (canonical_token, True) when the transducer recognizes it, or 
    (term, False) when it does not, so an unknown term is flagged and never silently thrown away"""

    characters = list(term.strip().lower())
    outputs = _translate(transducer, characters)
    if outputs and outputs[0]:
        return str(_plain(outputs[0][0])), True
    return term, False

def normalize_all(terms, profile):

    """Normalizes the whole raw list for one profile, keeping duplicates and unrecognized terms in the same order they came in"""

    transducer = build_transducer(profile)
    return [normalize_term(term, transducer)[0] for term in terms]

def canonical_order(profile):

    """Returns the profile groups in the order used to sort technologies.
    For example, Full Stack uses Frontend, Backend, Database, and Version control"""

    groups = []
    for group, _, _ in PROFILES[profile]:
        if group not in groups:
            groups.append(group)
    return groups


def sort_normalized(terms, profile):

    """Puts the normalized terms in the canonical order of the profile.
    Repeated terms are collapsed, and anything that is not part of the
    profile (unrecognized terms or qualifications of another profile) is
    left out, so the result only has the alphabet of that profile's automaton
    and no longer depends on how the resume was written"""

    rank = token_rank(profile)
    relevant = {term for term in terms if term in rank}
    return sorted(relevant, key=lambda term: rank[term])