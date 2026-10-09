# Formalization

This document defines the formal objects that Stage 2 and Stage 3 of the pipeline are built from, so that build_transducer and build_automaton in module-design.md have an explicit, named structure to implement from instead of an informal description. It follows the same notation covered in class, one tuple shape per model, and one section per supported profile, in the same order the rest of the project uses them.

## Finite-state transducer

The normalization step in Stage 2 is modeled, for each profile, as a finite-state transducer M = (Q, Sigma, Gamma, q0, F, delta, sigma). Q is the finite set of states the transducer moves through while reading one raw qualification string. Sigma is the input alphabet, the raw spellings Stage 1 can produce for that profile, such as JS or React.js. Gamma is the output alphabet, the canonical tokens those spellings are meant to collapse into, such as JAVASCRIPT or REACT. q0 is the initial state the transducer starts in before reading anything, F is the set of final states, reached once a full raw string has been consumed and a canonical token is ready to be emitted, delta is the transition function Q x Sigma -> Q, and sigma is the output function Q x Sigma -> Gamma, read together once per input symbol as the transducer advances.

Framed this way, normalize_term from module-design.md is exactly running one raw string through this transducer from q0 to a state in F and reading off the output sigma produced along the way; a string that never reaches F is the unrecognized case that function already accounts for.

## Finite automaton

The recognition step in Stage 3 is modeled, for each profile, as a deterministic finite automaton A = (Q, Sigma, q0, F, delta). Here Sigma is not the raw spellings anymore but the canonical tokens Stage 2 produces, in the fixed category order canonical_order defines for that profile. Q is the finite set of states the automaton passes through while reading that ordered sequence, q0 is its initial state, F is the set of accepting states, and delta is the transition function Q x Sigma -> Q. A sequence is accepted exactly when reading it from q0 ends in a state that belongs to F, which is what accepts in module-design.md is expected to return.

## Full Stack Developer

The concrete transducer and automaton for this profile, including their state sets and transition tables, will be written here once Stage 2 and Stage 3 are implemented for it. The input alphabet Sigma for the transducer follows from the raw spellings already listed in technical_skills.py; the canonical alphabet Gamma and the accepted ordering follow from canonical_order as described in module-design.md.

## Machine Learning Engineer

Same as above, pending the implementation of Stage 2 and Stage 3 for this profile.

## DevOps Engineer

Same as above, pending the implementation of Stage 2 and Stage 3 for this profile.

## Data Engineer

Same as above, pending the implementation of Stage 2 and Stage 3 for this profile.
