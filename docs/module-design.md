# Module Design

This document covers the second part of the design deliverable: the functions each module exposes, with their inputs and outputs. It assumes the pipeline and data flow described in architecture.md and gives the concrete signatures that follow from it.

## Stage 1: extraction (src/stage1_extraction)

extract_contact_info(text) takes the raw resume text and returns a dictionary with whatever contact fields the regular expressions recognize, such as email and phone number. A field that is not found is simply left out rather than filled with a placeholder.

extract_programming_languages(text), extract_frameworks(text), extract_databases(text), extract_tools(text) and extract_other_qualifications(text) each take the raw resume text and return a list of the raw substrings matched by that field's regular expression, in the order they appear in the text. These lists are not checked against each other, so the same technology mentioned twice produces two entries; deduplication is left to Stage 2, since it already has to decide which strings are equivalent. extract_other_qualifications covers phrases named in the reference profiles that are not a single technology name, such as REST APIs and Machine-learning model development.

extract_education(text) and extract_experience(text) take the raw resume text and each return a list of dictionaries, one per entry found (one per degree, one per job), since the guide asks the DSL in Stage 4 to support repeated elements such as multiple education records or multiple experiences.

extract_all(text) calls every function above and returns a single object, ResumeData, that groups their results. This is the only function Stage 1 exposes to the rest of the pipeline; the individual extractors exist so each regular expression can be defined, explained and tested on its own, which is also what the guide asks for in this stage.

## Stage 2: normalization (src/stage2_normalization)

build_transducer(profile) takes a profile name and returns the finite-state transducer for that profile, built with pyformlang from the 7-tuple defined for it in the formalization document. Building the transducer is kept separate from applying it so the same transducer object can be reused across many resumes instead of being rebuilt every time.

normalize_term(term, transducer) takes one raw string, such as "JS", and the transducer for the relevant profile, and returns the single canonical token it maps to, such as JAVASCRIPT. If the term is not recognized by the transducer, the function returns it unchanged and flags it as unrecognized rather than discarding it silently.

normalize_all(terms, profile) takes the raw qualification list from Stage 1 and a profile name, builds or reuses that profile's transducer, and returns the list of canonical tokens, preserving duplicates and unrecognized terms exactly as normalize_term would produce them one at a time.

canonical_order(profile) takes a profile name and returns the fixed category order defined for it, for example Frontend, Backend, Database, Version control for Full Stack Developer.

sort_normalized(terms, profile) takes the normalized list from normalize_all and the profile name, and returns that list reordered according to canonical_order, which is the representation Stage 3 expects as input.

## Stage 3: recognition (src/stage3_recognition)

build_automaton(profile) takes a profile name and returns the finite automaton for that profile, built with pyformlang from the 5-tuple defined for it in the formalization document, in the same spirit as build_transducer above.

accepts(sequence, profile) takes the normalized, ordered sequence produced by Stage 2 for one profile and that profile's automaton, and returns a boolean: true if the sequence is accepted by the automaton, false otherwise. No partial or probabilistic result is returned, since the guide frames this stage as a membership question, not a ranking.

classify(sequence_by_profile) takes a dictionary mapping each of the four profiles to the sequence Stage 2 produced for that profile, and returns a dictionary mapping each profile to its accepts result, which is the structure Stage 4 expects as its classification input.

## Stage 4: grammar (src/stage4_grammar)

build_profile_text(resume_data, normalized_by_profile, classification) takes the Stage 1 output, the Stage 2 output for every profile and the Stage 3 classification dictionary, and returns a single string written in the concrete syntax of the candidate profile DSL, ready to be parsed.

validate_profile(profile_text) takes that string, parses it with the textX grammar, and returns the resulting model object if the text is syntactically and lexically valid. If it is not, the function raises an error describing which rule was violated instead of returning a partial model.

render_html(model) and render_markdown(model) each take a validated model and return a string: a short HTML page in the first case, in the same spirit as the example in the guide, and a Markdown document in the second.

## Orchestrator (src/pipeline.py)

run_pipeline(resume_text, profiles) takes the raw resume text and the list of profiles to check it against (normally all four), and returns the final visualization string. Internally it calls extract_all once, then normalize_all, sort_normalized and build_automaton plus accepts once per profile, then classify, and finally build_profile_text, validate_profile and render_html or render_markdown. This is the single entry point the user interface and the tests are expected to call; nothing outside pipeline.py should need to import from more than one stage package at a time.
